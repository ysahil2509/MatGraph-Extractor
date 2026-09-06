"""
Native PDF Table Extractor for MatGraph Extractor.
Extracts tabular structures, headers, and text from scientific PDF publications using pdfplumber and PyMuPDF (fitz).
"""

import os
import pandas as pd
from typing import List, Dict, Any, Optional

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import fitz # PyMuPDF
except ImportError:
    fitz = None

class PDFTableExtractor:
    """
    Extracts tabular data directly from research paper PDFs.
    """

    def __init__(self):
        self.has_pdfplumber = pdfplumber is not None
        self.has_fitz = fitz is not None

    def extract_tables_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extracts all tables detected across all pages of a PDF file."""
        if not os.path.exists(pdf_path):
            return [{"error": f"File not found: {pdf_path}"}]

        extracted_tables = []
        filename = os.path.basename(pdf_path)
        paper_id = os.path.splitext(filename)[0]

        if self.has_pdfplumber:
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_idx, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        for tbl_idx, raw_table in enumerate(tables):
                            if not raw_table or len(raw_table) < 2:
                                continue

                            # Standardize headers and rows
                            headers = [str(c).strip() if c else f"Col_{i+1}" for i, c in enumerate(raw_table[0])]
                            data_rows = []
                            for row in raw_table[1:]:
                                clean_row = [str(c).strip() if c else "-" for c in row]
                                if any(clean_row):
                                    data_rows.append(clean_row)

                            if data_rows:
                                max_cols = len(headers)
                                padded_rows = [r[:max_cols] + ["-"] * max(0, max_cols - len(r)) for r in data_rows]
                                df_cleaned = pd.DataFrame(padded_rows, columns=headers)

                                extracted_tables.append({
                                    "paper_id": paper_id,
                                    "table_id": f"pdf_p{page_idx+1}_t{tbl_idx+1}",
                                    "page_number": page_idx + 1,
                                    "caption": f"Table on Page {page_idx+1} of {filename}",
                                    "footnote": "",
                                    "num_rows": len(padded_rows),
                                    "num_cols": max_cols,
                                    "headers": headers,
                                    "cleaned_records": df_cleaned.to_dict(orient="records"),
                                    "cleaned_df": df_cleaned
                                })
            except Exception as e:
                print(f"[PDF Extractor] Error processing {pdf_path}: {e}")

        return extracted_tables

if __name__ == "__main__":
    extractor = PDFTableExtractor()
    print("PDF Table Extractor initialized. pdfplumber available:", extractor.has_pdfplumber)
