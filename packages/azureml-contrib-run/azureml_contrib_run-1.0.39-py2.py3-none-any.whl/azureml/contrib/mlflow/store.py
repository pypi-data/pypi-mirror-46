# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowStore** provides a class to read and record run metrics and artifacts on Azure via MLflow."""

import json
import logging
import os
import time

from mlflow.utils.proto_json_utils import parse_dict
from mlflow.store.rest_store import RestStore
from mlflow.utils.rest_utils import MlflowHostCreds, http_request, _can_parse_as_json
from mlflow.exceptions import RestException, MlflowException
from mlflow.store.rest_store import _METHOD_TO_INFO

from azureml.core import Workspace
from azureml.core.authentication import AzureMLTokenAuthentication

from azureml._restclient.clientbase import DEFAULT_BACKOFF, DEFAULT_RETRIES
from azureml._restclient.run_client import RunClient

logger = logging.getLogger(__name__)

PARAM_PREFIX = "azureml.param."

_EXPERIMENT_NAME_ENV_VAR = "MLFLOW_EXPERIMENT_NAME"
_MLFLOW_RUN_ID_ENV_VAR = "MLFLOW_RUN_ID"


class AzureMLRestException(RestException):
    """Exception thrown on non 200-level responses from the REST API."""

    # WARNING TODO Original from commit: be631b266112efa5328de26e51acf70d6858ca44 with single edit
    def __init__(self, json, *args, **kwargs):
        """Exception thrown on non 200-level responses from the REST API. Supports default error_code."""
        error_code = json.get('error_code')  # Edit is to use get instead, and allow defaults through inheritence
        message = "Response body: '{}'".format(json)  # Edit to not drop errors if "message" is not in json
        if 'message' in json:
            message = "%s: %s" % (error_code, json['message'])
        # The below use of RestException is done to call its super's init: MlflowException.__init__
        super(RestException, self).__init__(message, error_code=error_code)
        self.json = json
        # WARNING TODO Remove this once above change is no longer needed


# WARNING function from commit be631b266112efa5328de26e51acf70d6858ca44, with a custom Exception
def http_request_safe(host_creds, endpoint, **kwargs):
    """Wrap ``http_request`` and also verifies that the request succeeds with code 200."""
    response = http_request(host_creds=host_creds, endpoint=endpoint, **kwargs)
    if response.status_code != 200:
        base_msg = "API request to endpoint %s failed with error code " \
                   "%s != 200" % (endpoint, response.status_code)
        if _can_parse_as_json(response.text):
            raise AzureMLRestException(json.loads(response.text))  # Changed from RestException to AzureMLRestException
        raise MlflowException("%s. Response body: '%s'" % (base_msg, response.text))
    return response
# WARNING end of function from commit be631b266112efa5328de26e51acf70d6858ca44, with a custom Exception


class AzureMLRestStore(RestStore):
    """Client for a remote tracking server accessed via REST API calls."""

    def __init__(self, workspace=None, artifact_uri=None):
        """Construct an AzureMLRestStore object."""
        self._artifact_uri = artifact_uri
        self.workspace = workspace if workspace is not None else Workspace.from_config()
        self.get_host_creds = self.get_host_credentials
        super(AzureMLRestStore, self).__init__(self.get_host_creds)

    def get_host_credentials(self):
        """Construct a MlflowHostCreds to be used for obtaining fresh credentials."""
        return MlflowHostCreds(
            self.workspace.service_context._get_run_history_url() +
            "/history/v1.0" + self.workspace.service_context._get_workspace_scope(),
            token=self.workspace._auth.get_authentication_header()["Authorization"][7:])

    # WARNING function from commit be631b266112efa5328de26e51acf70d6858ca44, used in _call_endpoint override
    # Written out here to support overriding http_request_safe
    def _original_call_endpoint(self, api, json_body):
        endpoint, method = _METHOD_TO_INFO[api]
        response_proto = api.Response()
        # Convert json string to json dictionary, to pass to requests
        if json_body:
            json_body = json.loads(json_body)
        host_creds = self.get_host_creds()

        if method == 'GET':
            response = http_request_safe(
                host_creds=host_creds, endpoint=endpoint, method=method, params=json_body)
        else:
            response = http_request_safe(
                host_creds=host_creds, endpoint=endpoint, method=method, json=json_body)

        js_dict = json.loads(response.text)
        parse_dict(js_dict=js_dict, message=response_proto)
        return response_proto
    # WARNING end of function from commit be631b266112efa5328de26e51acf70d6858ca44, used in _call_endpoint override

    def _call_endpoint(self, *args, **kwargs):
        total_retry = DEFAULT_RETRIES
        backoff = DEFAULT_BACKOFF
        for i in range(total_retry):
            try:
                return self._original_call_endpoint(*args, **kwargs)
            except AzureMLRestException as rest_exception:
                more_retries_left = i < total_retry - 1
                is_throttled = rest_exception.json.get("error", {"code": 0}).get("code") == "RequestThrottled"
                if more_retries_left and is_throttled:
                    logger.debug("There were too many requests. Try again soon.")
                    self._wait_for_retry(backoff, i, total_retry)
                else:
                    raise

    @classmethod
    def _wait_for_retry(cls, back_off, left_retry, total_retry):
        delay = back_off * 2 ** (total_retry - left_retry - 1)
        time.sleep(delay)

    def create_run(self, *args, **kwargs):
        """Create a run and set the AzureMLTokenAuthentication in the workspace."""
        run = super(AzureMLRestStore, self).create_run(*args, **kwargs)
        if not isinstance(self.workspace._auth, AzureMLTokenAuthentication) and _EXPERIMENT_NAME_ENV_VAR in os.environ:
            run_uuid = run.info.run_uuid
            experiment_name = os.environ[_EXPERIMENT_NAME_ENV_VAR]
            run_client = RunClient(self.workspace.service_context, experiment_name, run_uuid)
            token = run_client.get_token().token
            auth_object = AzureMLTokenAuthentication.create(
                azureml_access_token=token,
                expiry_time=None,
                host=self.workspace.service_context._get_run_history_url(),
                subscription_id=self.workspace.subscription_id,
                resource_group_name=self.workspace.resource_group,
                workspace_name=self.workspace.name,
                experiment_name=experiment_name,
                run_id=run_uuid
            )
            self.workspace._auth = auth_object

        return run
