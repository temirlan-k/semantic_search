from unittest.mock import MagicMock
import pytest
from src.application.use_cases.user.user import (
    UserUseCase,
)


@pytest.fixture
def user_use_case(mock_tm, mock_settings):
    return UserUseCase(
        transaction_manager_factory=mock_tm, security_settings=mock_settings
    )


@pytest.mark.asyncio
async def test_register_user_success(user_use_case, mock_repo, mocker):
    mocker.patch(
        "src.application.use_cases.user.user.hash_password",
        return_value="hashed_123",
    )

    mock_repo.get_user_by_username.return_value = None
    mock_repo.create_user.return_value = MagicMock(id=7, username="test")

    response = await user_use_case.register_user(
        {
            "username": "test",
            "password": "123",
        }
    )

    assert response == {
        "message": "User registered successfully",
        "user_id": 7,
    }

    mock_repo.get_user_by_username.assert_called_once_with("test")
    mock_repo.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_authenticate_user_success(user_use_case, mock_repo, mocker):
    mocker.patch(
        "src.application.use_cases.user.user.verify_password",
        return_value=True,
    )
    mocker.patch(
        "src.application.use_cases.user.user.create_access_token",
        return_value="token",
    )

    mock_repo.get_user_by_username.return_value = MagicMock(
        id=7,
        hashed_password="hashed_pw",
    )

    response = await user_use_case.authenticate_user(
        {
            "username": "test",
            "password": "123",
        }
    )

    assert response["access_token"] == "token"
    assert response["token_type"] == "Bearer"
    assert response["expires_in"] == (
        user_use_case._security_settings.jwt_access_token_expire_minutes * 60
    )

    mock_repo.get_user_by_username.assert_called_once_with("test")
