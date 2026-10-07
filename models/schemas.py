from datetime import date
from typing import List

from pydantic import BaseModel, Field


class LogisticsDocument(BaseModel):
    """
    Information extracted from a logistics/business document.
    """

    company_name: str | None = Field(default=None)

    address: str | None = Field(default=None)

    phone_numbers: List[str] = Field(
        default_factory=list
    )

    emails: List[str] = Field(
        default_factory=list
    )

    gst_number: str | None = Field(default=None)

    document_type: str | None = Field(default=None)

    invoice_number: str | None = Field(default=None)

    invoice_date: str | None = Field(default=None)

    bank_name: str | None = Field(default=None)

    account_number: str | None = Field(default=None)

    ifsc_code: str | None = Field(default=None)


class CustomerCreate(BaseModel):
    """
    Data required to create a customer.
    """

    company_name: str

    address: str | None = None

    phone_numbers: List[str] = Field(
        default_factory=list
    )

    emails: List[str] = Field(
        default_factory=list
    )

    gst_number: str | None = None