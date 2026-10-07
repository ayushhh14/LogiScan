import json
import tempfile
from pathlib import Path

import streamlit as st

from database.database import create_tables
from database.repository import (
    get_or_create_customer,
    save_document,
)

from extraction.structured_extractor import LLMExtractor
from ocr.extractor import extract_text


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="OCR-LogiScan",
    page_icon="📄",
    layout="wide",
)


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

create_tables()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📄 OCR-LogiScan")

st.markdown(
    """
    ### LogiScan: Intelligent Document Information Extraction

    Upload a logistics document, invoice, or business document
    and automatically extract important customer and document
    information using OCR and Gemini AI.
    """
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ System")

    st.success("Database connected")

    st.info(
        "Upload a document to begin processing."
    )

    st.markdown(
        """
        **Supported formats**

        - PDF
        - PNG
        - JPG / JPEG
        - WEBP
        """
    )


# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a logistics document",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "webp",
    ],
)


# --------------------------------------------------
# Process Document
# --------------------------------------------------

if uploaded_file:

    st.divider()

    st.subheader("📎 Selected Document")

    st.write(
        f"**File:** {uploaded_file.name}"
    )

    st.write(
        f"**Size:** "
        f"{uploaded_file.size / 1024:.2f} KB"
    )

    process_button = st.button(
        "🚀 Process Document",
        type="primary",
        use_container_width=True,
    )

    if process_button:

        # ------------------------------------------
        # Save uploaded file temporarily
        # ------------------------------------------

        suffix = Path(
            uploaded_file.name
        ).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_file_path = temp_file.name

        try:

            # --------------------------------------
            # OCR
            # --------------------------------------

            with st.spinner(
                "🔍 Extracting text using OCR..."
            ):

                ocr_text = extract_text(
                    temp_file_path
                )

            if not ocr_text:

                st.error(
                    "No text could be extracted "
                    "from this document."
                )

                st.stop()

            st.success(
                "OCR extraction completed."
            )

            # --------------------------------------
            # Gemini
            # --------------------------------------

            with st.spinner(
                "🤖 Analyzing document with Gemini..."
            ):

                extractor = LLMExtractor()

                structured_data = (
                    extractor.extract(
                        ocr_text
                    )
                )

            st.success(
                "Information extraction completed."
            )

            # --------------------------------------
            # Customer
            # --------------------------------------

            with st.spinner(
                "👤 Identifying customer..."
            ):

                customer = (
                    get_or_create_customer(
                        structured_data
                    )
                )

            # --------------------------------------
            # Database
            # --------------------------------------

            with st.spinner(
                "💾 Saving document..."
            ):

                document = save_document(
                    data=structured_data,
                    customer_id=customer.id,
                    source_file=uploaded_file.name,
                    raw_ocr_text=ocr_text,
                )

            st.success(
                "Document successfully stored."
            )

            # --------------------------------------
            # Results
            # --------------------------------------

            st.divider()

            st.header(
                "📊 Extraction Results"
            )

            # Customer information

            st.subheader(
                "👤 Customer Information"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Customer ID**"
                )

                st.write(
                    customer.id
                )

                st.write(
                    "**Company Name**"
                )

                st.write(
                    structured_data.company_name
                )

                st.write(
                    "**Address**"
                )

                st.write(
                    structured_data.address
                )

            with col2:

                st.write(
                    "**Phone Numbers**"
                )

                st.write(
                    structured_data.phone_numbers
                )

                st.write(
                    "**Emails**"
                )

                st.write(
                    structured_data.emails
                )

                st.write(
                    "**GST Number**"
                )

                st.write(
                    structured_data.gst_number
                )

            # --------------------------------------
            # Document information
            # --------------------------------------

            st.subheader(
                "📄 Document Information"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Document ID",
                    document.id,
                )

            with col2:

                st.write(
                    "**Document Type**"
                )

                st.write(
                    structured_data.document_type
                )

            with col3:

                st.write(
                    "**Invoice Number**"
                )

                st.write(
                    structured_data.invoice_number
                )

            st.write(
                "**Invoice Date:**",
                structured_data.invoice_date,
            )

            # --------------------------------------
            # Banking information
            # --------------------------------------

            st.subheader(
                "🏦 Banking Information"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    "**Bank Name**"
                )

                st.write(
                    structured_data.bank_name
                )

            with col2:

                st.write(
                    "**Account Number**"
                )

                st.write(
                    structured_data.account_number
                )

            with col3:

                st.write(
                    "**IFSC Code**"
                )

                st.write(
                    structured_data.ifsc_code
                )

            # --------------------------------------
            # Raw OCR
            # --------------------------------------

            with st.expander(
                "🔍 View Raw OCR Text"
            ):

                st.text(
                    ocr_text
                )

            # --------------------------------------
            # JSON
            # --------------------------------------

            json_data = (
                structured_data.model_dump()
            )

            json_string = json.dumps(
                json_data,
                indent=4,
                ensure_ascii=False,
            )

            with st.expander(
                "🧾 View Structured JSON"
            ):

                st.json(
                    json_data
                )

            # --------------------------------------
            # Download
            # --------------------------------------

            st.download_button(
                label="⬇️ Download JSON",
                data=json_string,
                file_name=(
                    f"{Path(uploaded_file.name).stem}"
                    "_result.json"
                ),
                mime="application/json",
                use_container_width=True,
            )

        except Exception as error:

            st.error(
                f"Processing failed: {error}"
            )

        finally:

            # --------------------------------------
            # Cleanup temporary file
            # --------------------------------------

            try:

                Path(
                    temp_file_path
                ).unlink(
                    missing_ok=True
                )

            except Exception:

                pass