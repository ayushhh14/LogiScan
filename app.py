import sys
from pathlib import Path

from database.database import create_tables
from database.repository import (
    get_or_create_customer,
    save_document,
)

from extraction.structured_extractor import LLMExtractor 
from ocr.extractor import extract_text
from utils.file_handler import save_json


def process_document(file_path: str):

    print("\n======================================")
    print("         OCR-LOGISCAN SYSTEM")
    print("======================================\n")

    # ----------------------------------
    # 1. Create database tables
    # ----------------------------------

    print("[1/6] Initializing database...")

    create_tables()

    print("      Database ready.")

    # ----------------------------------
    # 2. OCR
    # ----------------------------------

    print("[2/6] Extracting text using OCR...")

    ocr_text = extract_text(
        file_path
    )

    if not ocr_text:

        raise ValueError(
            "No text could be extracted "
            "from the document."
        )

    print("      OCR extraction completed.")

    # ----------------------------------
    # 3. Gemini extraction
    # ----------------------------------

    print(
        "[3/6] Extracting structured "
        "information using Gemini..."
    )

    extractor = LLMExtractor()

    structured_data = extractor.extract(
        ocr_text
    )

    print(
        "      Structured extraction completed."
    )

    # ----------------------------------
    # 4. Customer matching
    # ----------------------------------

    print(
        "[4/6] Identifying customer..."
    )

    customer = get_or_create_customer(
        structured_data
    )

    print(
        f"      Customer ID: {customer.id}"
    )

    # ----------------------------------
    # 5. Save document
    # ----------------------------------

    print(
        "[5/6] Saving document to database..."
    )

    document = save_document(
        data=structured_data,
        customer_id=customer.id,
        source_file=file_path,
        raw_ocr_text=ocr_text,
    )

    print(
        f"      Document ID: {document.id}"
    )

    # ----------------------------------
    # 6. Save JSON
    # ----------------------------------

    print(
        "[6/6] Saving structured JSON..."
    )

    input_path = Path(file_path)

    output_path = (
        Path("data/output")
        / f"{input_path.stem}_result.json"
    )

    save_json(
        structured_data,
        str(output_path)
    )

    print(
        f"      JSON saved to: {output_path}"
    )

    # ----------------------------------
    # Summary
    # ----------------------------------

    print("\n======================================")
    print("          EXTRACTION SUMMARY")
    print("======================================")

    print(
        f"Customer ID : {customer.id}"
    )

    print(
        f"Customer    : {customer.company_name}"
    )

    print(
        f"Document ID : {document.id}"
    )

    print(
        f"Output      : {output_path}"
    )

    print("\nExtracted Information:")
    print("--------------------------------------")

    for field, value in (
        structured_data.model_dump().items()
    ):

        print(
            f"{field}: {value}"
        )

    print("\n======================================")
    print("        PROCESS COMPLETED")
    print("======================================\n")


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python app.py <path_to_document>"
        )

        sys.exit(1)

    document_path = sys.argv[1]

    process_document(
        document_path
    )