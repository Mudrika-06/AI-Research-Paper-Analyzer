import fitz


def extract_pdf_pages(pdf_file):

    pages = []

    try:

        pdf = fitz.open(
            stream=pdf_file,
            filetype="pdf"
        )

        for index, page in enumerate(pdf):

            text = page.get_text("text")

            if text.strip():

                pages.append({
                    "page": index + 1,
                    "text": text.strip()
                })

        pdf.close()

    except Exception as error:

        raise ValueError(
            f"Unable to read PDF: {error}"
        )

    if not pages:

        raise ValueError(
            "No readable text found in PDF. "
            "Scanned PDFs require OCR."
        )

    return pages


def get_document_statistics(pages):

    text = " ".join(
        page["text"] for page in pages
    )

    words = text.split()

    return {
        "pages": len(pages),
        "words": len(words),
        "characters": len(text),
        "paragraphs": len(text.split("\n\n"))
    }
