# (C) 2024 GoodData Corporation
import difflib
import json
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from env import WORKSPACE_ID
import gooddata_api_client
import pytest
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from gooddata_api_client.model.chat_request import ChatRequest
from utils import load_json, normalize_metrics

EXPECTED_OBJECTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_response")
QUESTIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fixtures")

questions_list = load_json(os.path.join(QUESTIONS_DIR, "ai_questions.json"))


class gooddataAiChatApp:
    def __init__(self, api_client, workspace_id):
        self.api_instance = smart_functions_api.SmartFunctionsApi(api_client)
        self.workspace_id = workspace_id

    async def ask_question(self, question: str):
        return self.api_instance.ai_chat(self.workspace_id, ChatRequest(question=question))

    async def chat_history(self, interaction_id: int, feedback: str):
        return self.api_instance.ai_chat_history(
            self.workspace_id, ChatHistoryRequest(chat_history_interaction_id=interaction_id, user_feedback=feedback)
        )


def print_diff(actual, expected, context):
    actual_str = json.dumps(actual, indent=4, sort_keys=True)
    expected_str = json.dumps(expected, indent=4, sort_keys=True)
    diff = difflib.unified_diff(
        expected_str.splitlines(), actual_str.splitlines(), fromfile="expected", tofile="actual", lineterm=""
    )
    print(f"\n{context} mismatch:")
    for line in diff:
        print(line)


def compare_and_print_diff(actual, expected, context):
    if actual != expected:
        print_diff(actual, expected, context)
    assert actual == expected, f"{context} mismatch"


def validate_response(actual_response, expected_response):
    actual_metrics = normalize_metrics(
        actual_response["created_visualizations"]["objects"][0]["metrics"], exclude_keys=["title"]
    )
    expected_metrics = normalize_metrics(expected_response["metrics"], exclude_keys=["title"])
    compare_and_print_diff(actual_metrics, expected_metrics, "Metrics")

    actual_visualization_type = actual_response["created_visualizations"]["objects"][0]["visualization_type"]
    expected_visualization_type = expected_response["visualizationType"]
    compare_and_print_diff(actual_visualization_type, expected_visualization_type, "Visualization type")

    actual_dimensionality = actual_response["created_visualizations"]["objects"][0]["dimensionality"]
    expected_dimensionality = expected_response["dimensionality"]
    compare_and_print_diff(actual_dimensionality, expected_dimensionality, "Dimensionality")

    actual_filters = actual_response["created_visualizations"]["objects"][0]["filters"]
    expected_filters = expected_response["filters"]
    compare_and_print_diff(actual_filters, expected_filters, "Filters")


@pytest.fixture(scope="module")
def app(set_authorization_header):  # Using the global fixture for Authorization header
    app_instance = gooddataAiChatApp(set_authorization_header, WORKSPACE_ID)
    return app_instance


@pytest.mark.parametrize(
    "question, expected_file",
    [(item["question"], item["expected_objects_file"]) for item in questions_list],
    ids=[item["question"] for item in questions_list],
)
@pytest.mark.asyncio
async def test_ai_chat(app, question, expected_file):
    expected_objects = load_json(os.path.join(EXPECTED_OBJECTS_DIR, expected_file))
    try:
        api_response = await app.ask_question(question)
        validate_response(api_response.to_dict(), expected_objects)

        interaction_id = api_response.chat_history_interaction_id
        user_feedback = await app.chat_history(interaction_id, "POSITIVE")
        assert isinstance(user_feedback, ChatHistoryResult), "Invalid response from chat history"
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    pytest.main()
