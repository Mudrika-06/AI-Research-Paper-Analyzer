
import fitz


def extract_pdf_text(uploaded_file):
    """Extract text and page information from a PDF."""

    try:
        pdf_bytes = uploaded_file.getvalue()

        if not pdf_bytes:
            raise ValueError("The uploaded PDF is empty.")

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages = []
        all_text = []

        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text("text").strip()

            pages.append({
                "page": page_number,
                "text": page_text
            })

            if page_text:
                all_text.append(page_text)

        page_count = len(document)
        document.close()

        full_text = "\n\n".join(all_text)

        if not full_text.strip():
            raise ValueError(
                "No selectable text was found. "
                "This may be a scanned PDF. OCR is not included."
            )

        return {
            "name": uploaded_file.name,
            "text": full_text,
            "pages": pages,
            "page_count": page_count,
            "word_count": len(full_text.split())
        }

    except Exception as error:
        raise ValueError(f"PDF processing failed: {error}")
