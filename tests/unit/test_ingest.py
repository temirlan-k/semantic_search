import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.use_cases.document.ingest_document import IngestDocumentUseCase


@pytest.fixture
def ingest_use_case(mock_tm, mock_ollama, mock_milvus):
    return IngestDocumentUseCase(
        transaction_manager_factory=mock_tm,
        ollama_service=mock_ollama,
        milvus_service=mock_milvus,
        pdf_parser=AsyncMock(),
    )


@pytest.mark.asyncio
async def test_ingest_document_success(
    ingest_use_case, mock_ollama, mock_repo, mock_milvus
):
    ingest_use_case.pdf_parser.extract_text.return_value = [(1, "content")]
    mock_ollama.generate_embeddings_batch.return_value = [[0.1]]
    mock_repo.create_document.return_value = MagicMock(
        id=1, uuid="550e8400-e29b-41d4-a716-446655440000"
    )

    result = await ingest_use_case.execute(
        user_id=1, filename="t.pdf", file_content=b"pdf"
    )

    assert result["document_id"] == 1
    mock_milvus.insert.assert_called_once()
