# (C) 2024 GoodData Corporation
# env.py
import os

# Define environment variables
HOST = os.getenv("GOODDATA_HOST", "https://testing.env.com")
TOKEN = os.getenv("GOODDATA_TOKEN", "")
DATASOURCE_ID = os.getenv("DATASOURCE_ID", "")
WORKSPACE_ID = "workspace_id"
