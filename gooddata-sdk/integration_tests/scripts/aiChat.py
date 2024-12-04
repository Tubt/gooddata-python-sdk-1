# (C) 2024 GoodData Corporation
import os
import sys
import pytest
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_result import ChatResult
from gooddata_api_client.model.chat_request import ChatRequest
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from pprint import pprint

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import WORKSPACE_ID, HOST, TOKEN


@pytest.fixture
def api_client():
    configuration = gooddata_api_client.Configuration(host=HOST)
    configuration.access_token = TOKEN
    with gooddata_api_client.ApiClient(configuration) as api_client:
        yield api_client


def test_ai_chat(api_client):
    question = "What is the number of Accounts?"

    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    chat_request = ChatRequest(question=question)

    try:
        api_response = api_instance.ai_chat(WORKSPACE_ID, chat_request)
        pprint(api_response)
        assert isinstance(api_response, ChatResult), "Response is not of type ChatResult"
    except gooddata_api_client.ApiException as e:
        print(f"Exception when calling SmartFunctionsApi->ai_chat: {e}")
        pytest.fail(f"Exception when calling SmartFunctionsApi->ai_chat: {e}\n")


def test_ai_chat_history(api_client):
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    chat_history_request = ChatHistoryRequest(
        chat_history_interaction_id=100,
        user_feedback="POSITIVE",
    )

    try:
        api_response = api_instance.ai_chat_history(WORKSPACE_ID, chat_history_request)
        pprint(api_response)
        assert isinstance(api_response, ChatHistoryResult), "Response is not of type ChatHistoryResult"
    except gooddata_api_client.ApiException as e:
        print(f"Exception when calling SmartFunctionsApi->ai_chat_history: {e}")
        print(f"Status Code: {e.status}")
        print(f"Reason: {e.reason}")
        print(f"HTTP response headers: {e.headers}")
        print(f"HTTP response body: {e.body}")
        pytest.fail(f"Exception when calling SmartFunctionsApi->ai_chat_history: {e}\n")


if __name__ == "__main__":
    pytest.main()
