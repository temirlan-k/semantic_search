from unittest.mock import MagicMock
import pytest
from src.application.use_cases.user.user import (
    UserUseCase,
    RegisterUserRequest,
    LoginRequest,
    TokenResponse,
)


@pytest.fixture
def user_use_case(mock_tm, mock_settings):
    return UserUseCase(
        transaction_manager_factory=mock_tm, security_settings=mock_settings
    )


@pytest.mark.asyncio
async def test_register_user_success(user_use_case, mock_repo, mocker):
    mocker.patch(
        "src.application.use_cases.user.user.hash_password", return_value="hashed_123"
    )
    mocker.patch(
        "src.application.use_cases.user.user.create_access_token", return_value="token"
    )

    mock_repo.get_user_by_username.return_value = None
    mock_repo.create_user.return_value = MagicMock(id=7, username="test")

    response = await user_use_case.register_user(
        RegisterUserRequest(username="test", password="123")
    )

    assert isinstance(response, TokenResponse)
    mock_repo.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_authenticate_user_success(user_use_case, mock_repo, mocker):
    mocker.patch(
        "src.application.use_cases.user.user.verify_password", return_value=True
    )
    mocker.patch(
        "src.application.use_cases.user.user.create_access_token", return_value="token"
    )

    mock_repo.get_user_by_username.return_value = MagicMock(id=7, hashed_password="pw")

    response = await user_use_case.authenticate_user(
        LoginRequest(username="test", password="123")
    )
    assert response.access_token == "token"
