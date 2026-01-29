from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from src.presentation.http.rest.api.v1.schemas.documents import (
    PDFIngestResponse,
    ChunkInfo,
    SearchRequest,
    SearchResponse,
    SearchResultItem,
)
from src.infrastructure.pdf.pdf_parser import PDFParser
from src.application.use_cases.document.ingest_document import IngestDocumentUseCase
from src.application.use_cases.document.search_documents import SearchDocumentsUseCase
from dependency_injector.wiring import inject, Provide
from main.di.container import Container

documents_router = APIRouter(prefix="/documents", tags=["documents"])


@documents_router.post("/ingest", response_model=PDFIngestResponse)
@inject
async def ingest_pdf(
    file: UploadFile = File(..., description="PDF файл"),
    chunk_size: int = Form(default=1000, description="Размер чанка"),
    chunk_overlap: int = Form(default=200, description="Перекрытие чанков"),
    preview_length: int = Form(
        default=0, description="Длина preview текста (0 = полный текст)"
    ),
    use_case: IngestDocumentUseCase = Depends(
        Provide[Container.ingest_document_use_case]
    ),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    if chunk_size < 100 or chunk_size > 2000:
        raise HTTPException(
            status_code=400, detail="chunk_size must be between 100 and 2000"
        )

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise HTTPException(
            status_code=400, detail="chunk_overlap must be between 0 and chunk_size"
        )

    file_content = await file.read()
    max_size = 50 * 1024 * 1024
    if len(file_content) > max_size:
        raise HTTPException(status_code=413, detail="File too large (max 50MB)")

    # TODO: Получать user_id из JWT токена
    user_id = 1

    # Вызываем use case (сохраняет в PostgreSQL + Milvus)
    result = await use_case.execute(
        user_id=user_id,
        filename=file.filename,
        file_content=file_content,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # Для preview формируем chunks снова (временно, пока не сохраняем текст в БД)
    parser = PDFParser()
    pages = await parser.extract_text(file_content)

    from src.infrastructure.pdf.text_chunker import TextChunker

    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = chunker.chunk_pages(pages)

    texts = [chunk.text for chunk in chunks]
    embeddings = await use_case.ollama.generate_embeddings_batch(texts, batch_size=5)

    chunk_infos = []
    for chunk, embedding in zip(chunks, embeddings):
        if preview_length > 0 and len(chunk.text) > preview_length:
            display_text = chunk.text[:preview_length] + "..."
        else:
            display_text = chunk.text

        chunk_infos.append(
            ChunkInfo(
                text=display_text,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                embedding_dim=len(embedding),
                char_count=len(chunk.text),
            )
        )

    return PDFIngestResponse(
        filename=file.filename,
        total_pages=result["total_pages"],
        total_chunks=result["chunks_count"],
        chunks=chunk_infos,
        embedding_model=use_case.ollama.model,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )


@documents_router.post("/search", response_model=SearchResponse)
@inject
async def search_documents(
    request: SearchRequest,
    use_case: SearchDocumentsUseCase = Depends(
        Provide[Container.search_documents_use_case]
    ),
):
    """
    🔍 Семантический поиск по документам (RAG)

    Генерирует эмбеддинг запроса и ищет похожие чанки в Milvus
    """
    result = await use_case.execute(
        query=request.query, top_k=request.top_k, threshold=request.threshold
    )

    search_results = [
        SearchResultItem(
            text=r["text"],
            filename=r["filename"],
            page_number=r["page_number"],
            chunk_index=r["chunk_index"],
            score=r["score"],
        )
        for r in result["results"]
    ]

    return SearchResponse(
        query=result["query"], results=search_results, total_found=result["total_found"]
    )
