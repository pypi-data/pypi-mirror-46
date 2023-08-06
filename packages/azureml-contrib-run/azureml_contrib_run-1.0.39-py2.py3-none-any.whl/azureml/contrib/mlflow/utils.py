# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""mlflow helper functions."""

import re

from azureml.core.authentication import ArmTokenAuthentication, AzureMLTokenAuthentication
from azureml.core import Workspace

from six.moves.urllib import parse

_IS_REMOTE = "is-remote"
_REGION = "region"
_SUB_ID = "sub-id"
_RES_GRP = "res-grp"
_WS_NAME = "ws-name"
_EXP_NAME = "experiment"
_RUN_ID = "runid"
_AUTH_HEAD = "auth-head"
_AUTH_TYPE = "auth-type"
_TRUE_QUERY_VALUE = "True"

_TOKEN_PREFIX = "Bearer "


def tracking_uri_decomp(path):
    """
    Parse the tracking URI into a dictionary.

    The tracking URI contains the scope information for the workspace.
    """
    regex = "/history\\/v1.0" \
        "\\/subscriptions\\/(.*)" \
        "\\/resourceGroups\\/(.*)" \
        "\\/providers\\/Microsoft.MachineLearningServices" \
        "\\/workspaces\\/(.*)"

    pattern = re.compile(regex)
    mo = pattern.match(path)

    ret = {}
    ret[_SUB_ID] = mo.group(1)
    ret[_RES_GRP] = mo.group(2)
    ret[_WS_NAME] = mo.group(3)

    return ret


def artifact_uri_decomp(path):
    """
    Parse the artifact URI into a dictionary.

    The artifact URI contains the scope information for the workspace, the experiment and the run_id.
    """
    regex = "/(.*)" \
        "\\/runs\\/(.*)\\/artifacts"

    pattern = re.compile(regex)
    mo = pattern.match(path)

    ret = {}
    ret[_EXP_NAME] = mo.group(1)
    ret[_RUN_ID] = mo.group(2)

    return ret


def get_workspace_from_url(parsed_url):
    """Create a Workspace object out of a parsed URL."""
    parsed_path = tracking_uri_decomp(parsed_url.path)
    subscription_id = parsed_path[_SUB_ID]
    resource_group_name = parsed_path[_RES_GRP]
    workspace_name = parsed_path[_WS_NAME]

    queries = parse.parse_qs(parsed_url.query)
    if _AUTH_HEAD not in queries:
        auth = None
    else:
        if queries[_AUTH_TYPE] == AzureMLTokenAuthentication.__class__.__name__:
            auth = AzureMLTokenAuthentication(
                queries[_AUTH_HEAD],
                host=parsed_url.netloc,
                subscription_id=subscription_id,
                resource_group_name=resource_group_name,
                workspace_name=workspace_name,
            )
        else:
            auth = ArmTokenAuthentication(queries[_AUTH_HEAD])

    return Workspace(subscription_id=subscription_id,
                     resource_group=resource_group_name,
                     workspace_name=workspace_name,
                     auth=auth)
