import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_repo():
    """Общий мок для всех репозиториев"""
    return AsyncMock()


@pytest.fixture
def mock_tm(mock_repo):
    """Мок менеджера транзакций с поддержкой контекстного менеджера"""
    tm = AsyncMock()
    # Привязываем репозитории (добавь другие, если появятся)
    tm.user_repository = mock_repo
    tm.document_repository = mock_repo

    # Имитируем 'async with tm:'
    tm.__aenter__.return_value = tm
    tm.__aexit__.return_value = None
    return tm


@pytest.fixture
def mock_ollama():
    """Мок сервиса Ollama"""
    mock = AsyncMock()
    mock.model = "llama3-test"
    return mock


@pytest.fixture
def mock_milvus():
    """Мок векторной базы Milvus"""
    return AsyncMock()


@pytest.fixture
def mock_settings():
    """Мок настроек безопасности"""
    settings = MagicMock()
    settings.jwt_access_token_expire_minutes = 30
    return settings
