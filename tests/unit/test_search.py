import pytest
from src.application.use_cases.document.search_documents import SearchDocumentsUseCase


@pytest.fixture
def search_use_case(mock_ollama, mock_milvus):
    return SearchDocumentsUseCase(
        ollama_service=mock_ollama, milvus_service=mock_milvus
    )


@pytest.mark.asyncio
async def test_search_execute_success(search_use_case, mock_ollama, mock_milvus):
    mock_ollama.generate_embedding.return_value = [0.1, 0.2, 0.3]
    mock_milvus.search.return_value = [{"id": 1, "score": 0.9, "text": "found"}]

    result = await search_use_case.execute(query="test query", top_k=1)

    assert result["query"] == "test query"
    assert len(result["results"]) == 1
    mock_ollama.generate_embedding.assert_called_once_with("test query")
    mock_milvus.search.assert_called_once()


@pytest.mark.asyncio
async def test_search_empty_results(search_use_case, mock_ollama, mock_milvus):
    mock_ollama.generate_embedding.return_value = [0.1] * 768
    mock_milvus.search.return_value = []

    result = await search_use_case.execute(query="nothing")

    assert result["total_found"] == 0
    assert result["results"] == []
