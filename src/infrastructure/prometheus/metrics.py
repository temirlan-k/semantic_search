# metrics.py
from prometheus_client import Counter, Histogram


documents_uploaded = Counter(
    "documents_uploaded_total", "Total number of documents uploaded"
)

pdf_indexing_time = Histogram(
    "pdf_indexing_duration_seconds", "Time spent indexing a PDF"
)

search_time = Histogram("search_duration_seconds", "Time spent on semantic search")
