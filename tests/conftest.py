import pytest
import os
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    """
    Initializes a test client for the FastAPI application.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def setup_test_env():
    """
    Configures environment variables for a clean test run.
    """
    os.environ["GEMINI_API_KEY"] = "test_key_placeholder"
    os.environ["MEDIA_UPLOAD_DIR"] = "./temp_test_media"
    yield
    # Cleanup temp test directory
    if os.path.exists("./temp_test_media"):
        import shutil
        shutil.rmtree("./temp_test_media")