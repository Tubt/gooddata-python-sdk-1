# (C) 2024 GoodData Corporation
import os
import sys

import pytest
from dotenv import load_dotenv
from gooddata_sdk import GoodDataSdk

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPTS_DIR)


# Load environment variables from the .env file
load_dotenv()

# Create the test_config dictionary with the loaded environment variables
test_config = {"host": os.getenv("HOST"), "token": os.getenv("TOKEN")}
workspace_id = os.getenv("WORKSPACE_ID")

questions = ["What is number of order line id ?"]
sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])


@pytest.mark.parametrize("question", questions)
def test_ask_ai(question):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    chat_ai_res = sdk.compute.ai_chat(workspace_id, question=question)

    print(f"Chat AI response: {chat_ai_res}")
    assert chat_ai_res is not None, "Response should not be None"

    print("before test")


if __name__ == "__main__":
    pytest.main()
