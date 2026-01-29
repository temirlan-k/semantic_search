import asyncio
import fitz  # PyMuPDF


class PDFParser:
    """Парсер для извлечения текста из PDF"""

    async def extract_text(self, pdf_bytes: bytes):
        return await asyncio.to_thread(self._extract_text_sync, pdf_bytes)

    def _extract_text_sync(self, pdf_bytes: bytes):
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            pages.append((page_num + 1, text))
        doc.close()
        return pages
