
import pdfplumber
from typing import List, Dict

def extract_text_from_pdf(file_path: str) -> List[Dict]:
    """
    Extracts text and tables from each page of the PDF.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        List[Dict]: A list of dictionaries with text and table content for each page
    """
    extracted_data = []

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_data = {}
            text = page.extract_text()
            tables = page.extract_tables()

            page_data["page_number"] = i + 1
            page_data["text"] = text if text else ""
            page_data["tables"] = tables if tables else []

            extracted_data.append(page_data)

    return extracted_data


def extract_full_text_only(file_path: str) -> str:
    """
    Extracts the entire PDF as a single string (no table info).

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Combined text from all pages
    """
    full_text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

    return "\n\n".join(full_text)
