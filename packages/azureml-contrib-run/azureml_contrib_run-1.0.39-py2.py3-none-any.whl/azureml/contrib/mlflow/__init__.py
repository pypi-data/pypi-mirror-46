# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Add the plugin handlers for the tracking and the artifact stores."""

import os
import logging
import re
from six.moves.urllib import parse

from functools import wraps

import mlflow
from mlflow.exceptions import MlflowException

import azureml
from azureml.exceptions import RunEnvironmentException
from azureml.core import Workspace, Experiment, Run
from azureml.core.authentication import ArmTokenAuthentication
from azureml.contrib.run._version import VERSION

from . import store
from .utils import get_workspace_from_url, _IS_REMOTE, _TRUE_QUERY_VALUE, _TOKEN_PREFIX

_SUBSCRIPTIONS_PREFIX = "/subscriptions/"

logger = logging.getLogger(__name__)

__version__ = VERSION

__all__ = ["get_portal_url", "register_model", "azureml_store_builder", "azureml_artifacts_builder"]


class _AzureMLStoreLoader(object):
    _azure_uri_to_store = {}

    @classmethod
    def _load_azureml_store(cls, store_uri, artifact_uri):
        # cache the Azure workspace object
        parsed_url = parse.urlparse(store_uri)
        #  Check if the URL is a test or prod AML URL
        queries = parse.parse_qs(parsed_url.query)
        if store_uri in cls._azure_uri_to_store:
            return cls._azure_uri_to_store[store_uri]
        elif _IS_REMOTE in queries and queries[_IS_REMOTE][0] == _TRUE_QUERY_VALUE:
            try:
                run = Run.get_context()
            except RunEnvironmentException:
                raise MlflowException(
                    "AzureMlflow tracking URI was set to remote but there was a failure in loading the run.")
            else:
                amlflow_store = store.AzureMLRestStore(
                    workspace=run.experiment.workspace, artifact_uri=artifact_uri)

                cls._azure_uri_to_store[store_uri] = amlflow_store
                mlflow.set_experiment(run.experiment.name)
        else:
            workspace = get_workspace_from_url(parsed_url)
            cls._azure_uri_to_store[store_uri] = store.AzureMLRestStore(
                workspace=workspace, artifact_uri=artifact_uri)

        return cls._azure_uri_to_store[store_uri]


def azureml_store_builder(store_uri=None, artifact_uri=None):
    """Create or return an AzureMLflowStore."""
    from mlflow.tracking.utils import get_tracking_uri
    tracking_uri = store_uri if store_uri is not None else get_tracking_uri()
    return _AzureMLStoreLoader._load_azureml_store(tracking_uri, artifact_uri)


def azureml_artifacts_builder(artifact_uri=None):
    """Create an AzureMLflowArtifactRepository."""
    from .artifact_repo import AzureMLflowArtifactRepository
    return AzureMLflowArtifactRepository(artifact_uri)


def _get_mlflow_tracking_uri(self, with_auth=True):
    """
    Retrieve the tracking URI from Workspace for use in AzureMLflow.

    Return a URI identifying the workspace, with optionally the auth header embeded
    as a query string within the URI as well. The authentication header does not include
    the "Bearer " prefix. Additionally, the URI will also contain experiment and run
    names and IDs if specified while calling this function.

    :return: Returns the URI pointing to this workspace, with the auth query paramter if
    with_auth is True.
    :rtype: str
    """
    queries = []
    if with_auth:
        auth = self._auth_object
        header = auth.get_authentication_header()
        token = header["Authorization"][len(_TOKEN_PREFIX):]
        queries.append("auth_type=" + auth.__class__.__name__)
        queries.append("auth=" + token)

    service_location = parse.urlparse(self.service_context._get_run_history_url()).netloc

    return "azureml://{}/history/v1.0{}?{}".format(
        service_location,
        self.service_context._get_workspace_scope(),
        "?" + "&".join(queries) if queries else "")


def _setup_remote(azureml_run):
    tracking_uri = azureml_run.experiment.workspace.get_mlflow_tracking_uri() + "&is-remote=True"
    mlflow.set_tracking_uri(tracking_uri)
    from mlflow.tracking.utils import _TRACKING_URI_ENV_VAR
    from mlflow.tracking.fluent import _RUN_ID_ENV_VAR
    os.environ[_TRACKING_URI_ENV_VAR] = tracking_uri
    os.environ[_RUN_ID_ENV_VAR] = azureml_run.id
    mlflow.set_experiment(azureml_run.experiment.name)
    from mlflow.entities import SourceType

    mlflow_tags = {}
    mlflow_source_type_key = 'mlflow.source.type'
    if mlflow_source_type_key not in azureml_run.tags:
        mlflow_tags[mlflow_source_type_key] = SourceType.to_string(SourceType.JOB),
    mlflow_source_name_key = 'mlflow.source.name'
    if mlflow_source_name_key not in azureml_run.tags:
        mlflow_tags[mlflow_source_name_key] = azureml_run.get_details()['runDefinition']['script']
    azureml_run.set_tags(mlflow_tags)


def get_portal_url(run):
    """Get the url to the Azure ML portal.

    :return: Returns the Azure portal url for the run.
    :rtype: str
    """
    if isinstance(run, Run):
        return run.get_portal_url()
    else:
        from mlflow.tracking.client import MlflowClient
        client = MlflowClient()
        experiment_name = client.get_experiment(run.info.experiment_id).name
        run_id = run.info.run_uuid
        host = MlflowClient().store.get_host_creds().host
        netloc = "https://mlworkspace.azure.ai/portal"
        uri = "{}{}".format(_SUBSCRIPTIONS_PREFIX, host.split(_SUBSCRIPTIONS_PREFIX, 2)[1])
        experiment_run_uri = "/experiments/{}/runs/{}".format(experiment_name, run_id)
        return netloc + uri + experiment_run_uri


def _azureml_run_from_mlflow_run(mlflow_run):
    from mlflow.tracking.client import MlflowClient
    client = MlflowClient()
    experiment_name = client.get_experiment(mlflow_run.info.experiment_id).name
    host = client.store.get_host_creds().host
    auth_token = client.store.get_host_creds().token

    cluster_url = host.split(_SUBSCRIPTIONS_PREFIX, 2)[0].split("/history/")[0]
    scope = "{}{}".format(_SUBSCRIPTIONS_PREFIX, host.split(_SUBSCRIPTIONS_PREFIX, 2)[1])
    auth = ArmTokenAuthentication(auth_token)
    run_id = mlflow_run.info.run_uuid

    subscription_id = re.search(r'/subscriptions/([^/]+)', scope).group(1)
    resource_group_name = re.search(r'/resourceGroups/([^/]+)', scope).group(1)
    workspace_name = re.search(r'/workspaces/([^/]+)', scope).group(1)
    workspace = Workspace(subscription_id,
                          resource_group_name,
                          workspace_name,
                          auth=auth,
                          _disable_service_check=True)

    experiment = Experiment(workspace, experiment_name)
    changed_env_var = False
    prev_env_var = None
    from azureml._base_sdk_common.service_discovery import HISTORY_SERVICE_ENDPOINT_KEY
    try:
        if HISTORY_SERVICE_ENDPOINT_KEY in os.environ:
            prev_env_var = os.environ[HISTORY_SERVICE_ENDPOINT_KEY]
        os.environ[HISTORY_SERVICE_ENDPOINT_KEY] = cluster_url
        changed_env_var = True
        azureml_run = Run(experiment, run_id)
        return azureml_run
    finally:
        if changed_env_var:
            if prev_env_var is not None:
                os.environ[HISTORY_SERVICE_ENDPOINT_KEY] = prev_env_var
            else:
                del os.environ[HISTORY_SERVICE_ENDPOINT_KEY]


@wraps(Run.register_model)
def register_model(run, *args, **kwargs):
    """Register a model with the specified name and logged artifact."""
    if isinstance(run, Run):
        azureml_run = run
    else:
        azureml_run = _azureml_run_from_mlflow_run(run)
    return azureml_run.register_model(*args, **kwargs)


azureml.core.workspace.Workspace.get_mlflow_tracking_uri = _get_mlflow_tracking_uri
