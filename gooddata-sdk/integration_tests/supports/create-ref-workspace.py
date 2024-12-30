# (C) 2024 GoodData Corporation
# filepath: /Users/tubui/Documents/CODE/gooddata-python-sdk-1/gooddata-sdk/integration_tests/supports/create-ref-workspace.py
import logging
import os
import sys

import gooddata_api_client
import pytest
from env import HOST
from gooddata_api_client.api import workspaces_entity_apis_api
from gooddata_api_client.model.json_api_workspace_in import JsonApiWorkspaceIn
from gooddata_api_client.model.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

configuration = gooddata_api_client.Configuration(host=HOST)
configuration.debug = True  # Enable debug logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class createEntityWorkspace:
    def __init__(self, api_client, host):
        self.api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)

    async def create_workspace(self, JsonApiWorkspaceInDocument):
        logger.info("0. Attempting to create workspace...")
        return await self.api_instance.create_entity_workspaces(JsonApiWorkspaceInDocument)


@pytest.fixture(scope="module")
def app(set_authorization_header):  # Using the global fixture for Authorization header
    app_instance = createEntityWorkspace(set_authorization_header)
    return app_instance


@pytest.mark.asyncio
async def test_create_workspace(app):
    logger.info("Attempting to create workspace...")
    json_api_workspace_in_document = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=JsonApiWorkspaceInAttributes(name="tu_sdk_test_name", description="Test description"),
            id="tu_sdk_test_id",
            type="workspace",
        ),
    )
    logger.info("JSON API Workspace In Document: %s", json_api_workspace_in_document)

    try:
        api_response = await app.create_workspace(json_api_workspace_in_document)
        logger.info("API Response: %s", api_response)
        if hasattr(api_response, "errors"):
            logger.error("API Errors: %s", api_response.errors)
    except gooddata_api_client.ApiException as e:
        logger.error("Exception: %s", e.body)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
