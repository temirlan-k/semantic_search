import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def mock_tm(mock_repo):
    tm = AsyncMock()
    tm.user_repository = mock_repo
    tm.document_repository = mock_repo

    tm.__aenter__.return_value = tm
    tm.__aexit__.return_value = None
    return tm


@pytest.fixture
def mock_ollama():
    mock = AsyncMock()
    mock.model = "nomic-embed-text"
    return mock


@pytest.fixture
def mock_milvus():
    return AsyncMock()


@pytest.fixture
def mock_settings():
    settings = MagicMock()
    settings.jwt_access_token_expire_minutes = 30
    return settings
