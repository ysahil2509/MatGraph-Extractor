"""
Automated downloader for scientific XML papers using Elsevier / ScienceDirect Article Retrieval API.
Reads ELSEVIER_API_KEY from environment variables or .env file to ensure secure API key handling.
"""

import os
import requests
import json
import time
from typing import List, Optional
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_BASE_URL = "https://api.elsevier.com/content/article/doi"

def download_paper_by_doi(doi: str, output_dir: str = "data/raw_xmls", api_key: Optional[str] = None) -> dict:
    """
    Downloads full-text XML for a given DOI from Elsevier ScienceDirect API.
    """
    key = api_key or os.getenv("ELSEVIER_API_KEY")
    if not key:
        return {
            "doi": doi,
            "status": "skipped",
            "reason": "Missing ELSEVIER_API_KEY environment variable. Please configure .env file."
        }

    headers = {
        "X-ELS-APIKey": key,
        "Accept": "text/xml"
    }

    url = f"{API_BASE_URL}/{doi}"
    os.makedirs(output_dir, exist_ok=True)
    safe_filename = doi.replace("/", "_").replace(".", "_") + ".xml"
    output_path = os.path.join(output_dir, safe_filename)

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            return {
                "doi": doi,
                "status": "success",
                "saved_to": output_path
            }
        else:
            return {
                "doi": doi,
                "status": "failed",
                "http_status": response.status_code,
                "reason": response.text[:200]
            }
    except Exception as e:
        return {
            "doi": doi,
            "status": "error",
            "reason": str(e)
        }

def batch_download_dois(doi_list: List[str], output_dir: str = "data/raw_xmls") -> list:
    """Batch downloads a list of DOIs with rate-limiting."""
    results = []
    for doi in doi_list:
        doi = doi.strip()
        if not doi:
            continue
        print(f"Fetching DOI: {doi}...")
        res = download_paper_by_doi(doi, output_dir)
        results.append(res)
        time.sleep(0.5)  # Rate limiting
    return results

if __name__ == "__main__":
    sample_dois = [
        "10.1016/j.msea.2023.144890",
        "10.1016/j.actamat.2023.118942"
    ]
    print("Testing DOI downloader...")
    out = batch_download_dois(sample_dois)
    print(json.dumps(out, indent=2))
