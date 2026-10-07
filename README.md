# OCR-LogiScan

OCR-LogiScan is an AI-powered logistics document processing system that automatically extracts important information from invoices, freight bills, shipping documents, and other business documents.

The system combines OCR, Large Language Models, structured data validation, and database storage to convert unstructured documents into structured and searchable information.

---

## Overview

Logistics and business documents often contain important information such as:

- Company details
- Addresses
- Phone numbers
- Email addresses
- GST numbers
- Invoice numbers
- Invoice dates
- Document types
- Bank details
- IFSC codes
- Account numbers

Manually extracting and organizing this information is time-consuming and error-prone.

OCR-LogiScan automates this process.

The system accepts PDF and image-based documents, extracts their text using OCR, sends the extracted text to an LLM through OpenRouter, validates the structured response using Pydantic, identifies the associated customer, and stores the information in a SQLite database.

---

## Key Features

- Upload PDF and image documents
- OCR-based text extraction
- Support for scanned PDFs
- AI-powered information extraction
- OpenRouter LLM integration
- Structured JSON generation
- Automatic customer identification
- Raw OCR text storage
- JSON result generation
- Streamlit web dashboard
- Download extracted JSON
- Display raw OCR text
- Display structured extraction results

---

### Tech Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **OCR:** Tesseract OCR, Pytesseract, Pillow
- **PDF Processing:** PyMuPDF
- **LLM / AI:** OpenRouter API
- **LLM Integration:** OpenAI Python SDK
- **Data Validation:** Pydantic
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Data Format:** JSON
- **Version Control:** Git & GitHub

