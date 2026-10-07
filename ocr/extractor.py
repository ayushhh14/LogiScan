from pathlib import Path

import pytesseract
from PIL import Image
import fitz


def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF.

    First attempts to extract existing text.
    If the PDF contains scanned pages, OCR can be
    applied to the rendered pages.
    """

    document = fitz.open(pdf_path)

    extracted_text = []

    for page in document:
        text = page.get_text()

        if text.strip():
            extracted_text.append(text)
        else:
            pixmap = page.get_pixmap()
            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples
            )

            ocr_text = pytesseract.image_to_string(image)

            extracted_text.append(ocr_text)

    document.close()

    return "\n".join(extracted_text).strip()


def extract_text(file_path: str) -> str:
    """
    Detect the file type and extract text accordingly.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension in [".png", ".jpg", ".jpeg", ".webp"]:
        return extract_text_from_image(file_path)

    elif extension == ".pdf":
        return extract_text_from_pdf(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )