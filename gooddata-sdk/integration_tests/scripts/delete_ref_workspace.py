# (C) 2024 GoodData Corporation
from workspace_manager import deleteWorkspace, HOST, TOKEN

if __name__ == "__main__":
    test_config = {"host": HOST, "token": TOKEN}

    deleteWorkspace(test_config)
