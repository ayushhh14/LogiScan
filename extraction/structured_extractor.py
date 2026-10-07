import json

from openai import OpenAI

from config.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)

from models.schemas import LogisticsDocument
from extraction.prompts import EXTRACTION_PROMPT


class LLMExtractor:

    def __init__(self):

        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def extract(self, ocr_text: str) -> LogisticsDocument:

        if not ocr_text.strip():
            raise ValueError("OCR text is empty.")

        prompt = EXTRACTION_PROMPT.format(
            ocr_text=ocr_text
        )

        response = self.client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        print("\n========== OPENROUTER RESPONSE ==========")
        print(response)
        print("=========================================\n")

        response_text = response.choices[0].message.content

        if not response_text:
            raise ValueError(
                "OpenRouter returned an empty response."
            )

        # -----------------------------------------
        # STEP 1: Parse JSON
        # -----------------------------------------

        try:
            data = json.loads(response_text)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"OpenRouter returned invalid JSON:\n{response_text}"
            ) from error

        # -----------------------------------------
        # STEP 2: Handle nested response
        # -----------------------------------------

        if (
            "customer_information" in data
            or "document_information" in data
            or "bank_information" in data
        ):

            customer_info = data.get(
                "customer_information",
                {}
            )

            document_info = data.get(
                "document_information",
                {}
            )

            bank_info = data.get(
                "bank_information",
                {}
            )

            data = {
                **customer_info,
                **document_info,
                **bank_info,
            }

        # -----------------------------------------
        # STEP 3: Validate using Pydantic
        # -----------------------------------------

        try:

            return LogisticsDocument.model_validate(data)

        except Exception as error:

            raise ValueError(
                f"OpenRouter returned valid JSON, "
                f"but it does not match the expected schema:\n"
                f"{data}"
            ) from error