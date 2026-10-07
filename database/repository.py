import json

from database.database import (
    Customer,
    Document,
    SessionLocal,
)
from models.schemas import LogisticsDocument


def find_customer(
    data: LogisticsDocument
):
    """
    Find an existing customer using GST number
    or company name.
    """

    db = SessionLocal()

    try:

        # GST is the strongest identifier
        if data.gst_number:

            customer = (
                db.query(Customer)
                .filter(
                    Customer.gst_number
                    == data.gst_number
                )
                .first()
            )

            if customer:
                return customer

        # Fallback to company name
        if data.company_name:

            customer = (
                db.query(Customer)
                .filter(
                    Customer.company_name
                    == data.company_name
                )
                .first()
            )

            if customer:
                return customer

        return None

    finally:
        db.close()


def create_customer(
    data: LogisticsDocument
):
    """
    Create a new customer record.
    """

    db = SessionLocal()

    try:

        customer = Customer(
            company_name=data.company_name
            or "Unknown",

            address=data.address,

            phone_numbers=json.dumps(
                data.phone_numbers
            ),

            emails=json.dumps(
                data.emails
            ),

            gst_number=data.gst_number
        )

        db.add(customer)

        db.commit()

        db.refresh(customer)

        return customer

    finally:
        db.close()


def save_document(
    data: LogisticsDocument,
    customer_id: int,
    source_file: str,
    raw_ocr_text: str
):
    """
    Save a document associated with a customer.
    """

    db = SessionLocal()

    try:

        document = Document(
            customer_id=customer_id,

            document_type=data.document_type,

            invoice_number=data.invoice_number,

            invoice_date=data.invoice_date,

            bank_name=data.bank_name,

            account_number=data.account_number,

            ifsc_code=data.ifsc_code,

            source_file=source_file,

            raw_ocr_text=raw_ocr_text
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        return document

    finally:
        db.close()


def get_or_create_customer(
    data: LogisticsDocument
):
    """
    Return an existing customer if found.
    Otherwise create a new customer.
    """

    customer = find_customer(data)

    if customer:

        print(
            f"Existing customer found: "
            f"{customer.company_name}"
        )

        return customer

    customer = create_customer(data)

    print(
        f"New customer created: "
        f"{customer.company_name}"
    )

    return customer