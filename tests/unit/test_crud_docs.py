import pytest
from unittest.mock import MagicMock
from src.application.use_cases.document.crud_document import CRUDDocumentUseCase
from src.domain.exceptions.exceptions import EntityNotFoundException


@pytest.fixture
def document_use_case(mock_tm, mock_milvus):
    return CRUDDocumentUseCase(
        transaction_manager_factory=mock_tm, milvus_service=mock_milvus
    )


@pytest.mark.asyncio
async def test_list_documents_success(document_use_case, mock_repo):
    doc_mock = MagicMock(uuid="uuid-1", filename="t.pdf", chunks_count=5, user_id=1)
    mock_repo.get_documents_by_user_id.return_value = [doc_mock]

    result = await document_use_case.list_documents(user_id=1)

    assert len(result) == 1
    assert result[0]["document_id"] == "uuid-1"
    mock_repo.get_documents_by_user_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_delete_document_success(document_use_case, mock_repo, mock_milvus):
    doc_mock = MagicMock(filename="test.pdf", user_id=1, chunks_count=10)
    mock_repo.get_document_by_id.return_value = doc_mock

    result = await document_use_case.delete_document(document_id=100, user_id=1)

    assert "successfully" in result["message"]
    mock_milvus.delete_by_filename.assert_called_once_with("test.pdf")
    mock_repo.delete_document.assert_called_once_with(100)


@pytest.mark.asyncio
async def test_delete_document_wrong_user(document_use_case, mock_repo):
    mock_repo.get_document_by_id.return_value = MagicMock(user_id=2)

    with pytest.raises(EntityNotFoundException):
        await document_use_case.delete_document(document_id=100, user_id=1)
