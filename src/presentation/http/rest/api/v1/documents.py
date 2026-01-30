from pydantic import UUID4
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from src.application.use_cases.document.crud_document import CRUDDocumentUseCase
from src.presentation.http.rest.api.v1.schemas.res.documents import (
    PDFIngestResponse,
    ChunkInfo,
)
from src.presentation.http.rest.api.v1.schemas.res.search import (
    SearchResponse,
    SearchResultItem,
)
from src.presentation.http.rest.api.v1.schemas.req.search import SearchRequest
from src.presentation.http.rest.api.v1.schemas.res.documents import (
    DocumentListItemResponse,
    DocumentListResponse,
    DeleteDocumentResponse,
)

from src.presentation.http.rest.api.v1.deps import get_current_user_id
from src.application.use_cases.document.ingest_document import IngestDocumentUseCase
from src.application.use_cases.document.search_documents import SearchDocumentsUseCase
from dependency_injector.wiring import inject, Provide
from main.di.container import Container

documents_router = APIRouter(prefix="/documents", tags=["documents"])


@documents_router.post("/upload", response_model=PDFIngestResponse)
@inject
async def ingest_pdf(
    file: UploadFile = File(..., description="PDF файл"),
    chunk_size: int = Form(default=1000, gt=100, lt=2000, description="Размер чанка"),
    chunk_overlap: int = Form(
        default=200, gt=0, lt=2000, description="Перекрытие чанков"
    ),
    current_user_id: int = Depends(get_current_user_id),
    use_case: IngestDocumentUseCase = Depends(
        Provide[Container.ingest_document_use_case]
    ),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_content = await file.read()

    result = await use_case.execute(
        user_id=current_user_id,
        filename=file.filename,
        file_content=file_content,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunk_infos = [ChunkInfo(**chunk) for chunk in result["chunks"]]

    return PDFIngestResponse(
        filename=result["filename"],
        total_pages=result["total_pages"],
        total_chunks=result["total_chunks"],
        chunks=chunk_infos,
        embedding_model=result["embedding_model"],
        chunk_size=result["chunk_size"],
        chunk_overlap=result["chunk_overlap"],
    )


@documents_router.post("/search", response_model=SearchResponse)
@inject
async def search_documents(
    request: SearchRequest,
    current_user_id: int = Depends(get_current_user_id),
    use_case: SearchDocumentsUseCase = Depends(
        Provide[Container.search_documents_use_case]
    ),
):
    result = await use_case.execute(
        query=request.query,
        top_k=request.top_k,
        threshold=request.threshold,
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


@documents_router.get("/list_documents", response_model=DocumentListResponse)
@inject
async def list_documents(
    current_user_id: int = Depends(get_current_user_id),
    use_case: CRUDDocumentUseCase = Depends(Provide[Container.crud_document_use_case]),
):
    documents_list = await use_case.list_documents(current_user_id)
    return {"documents": documents_list}


@documents_router.get("/{document_id}", response_model=DocumentListItemResponse)
@inject
async def get_document(
    document_id: UUID4,
    current_user_id: int = Depends(get_current_user_id),
    use_case: CRUDDocumentUseCase = Depends(Provide[Container.crud_document_use_case]),
):
    return await use_case.get_document(document_id, current_user_id)


@documents_router.delete("/{document_id}", response_model=DeleteDocumentResponse)
@inject
async def delete_document(
    document_id: UUID4,
    current_user_id: int = Depends(get_current_user_id),
    use_case: CRUDDocumentUseCase = Depends(Provide[Container.crud_document_use_case]),
):
    return await use_case.delete_document(document_id, current_user_id)
