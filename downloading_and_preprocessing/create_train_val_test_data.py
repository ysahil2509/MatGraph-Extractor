"""
Prepares train/validation/test data splits and tokenized sequences from extracted scientific tables.
Formatted for MatSciBERT sequence labeling and token classification tasks.
"""

import os
import json
import random
from typing import List, Dict, Any, Tuple

def generate_bio_tagged_tokens(table_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates BIO-tagged token sequences for tabular headers and rows.
    Identifies MATERIAL, COMPONENT, PERCENTAGE, PROPERTY, and UNIT tokens.
    """
    tagged_instances = []
    headers = table_dict.get("headers", [])
    records = table_dict.get("cleaned_records", [])

    # Process table headers
    for h in headers:
        tokens = h.split()
        tags = []
        is_prop = any(k in h.lower() for k in ["strength", "hardness", "density", "temp", "modulus", "conductivity", "voltage", "capacity", "strain"])
        is_comp = any(k in h.lower() for k in ["wt%", "at%", "mol%", "wt.", "at.", "mol.", "composition"])
        
        for i, tok in enumerate(tokens):
            if is_prop:
                tags.append("B-PROP" if i == 0 else "I-PROP")
            elif is_comp:
                tags.append("B-COMP" if i == 0 else "I-COMP")
            else:
                tags.append("O")

        tagged_instances.append({
            "source": "header",
            "text": h,
            "tokens": tokens,
            "tags": tags
        })

    # Process table rows
    for row in records:
        for k, v in row.items():
            val_str = str(v)
            tokens = val_str.split()
            tags = ["O"] * len(tokens)
            tagged_instances.append({
                "source": "cell",
                "header": k,
                "text": val_str,
                "tokens": tokens,
                "tags": tags
            })

    return tagged_instances

def create_dataset_splits(
    tables_json_path: str = "data/tables/extracted_tables_all.json",
    output_dir: str = "data/processed",
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    seed: int = 42
) -> Dict[str, int]:
    """Splits extracted tables into train, validation, and test sets."""
    if not os.path.exists(tables_json_path):
        return {"error": f"File not found: {tables_json_path}"}

    with open(tables_json_path, "r", encoding="utf-8") as f:
        tables = json.load(f)

    random.seed(seed)
    random.shuffle(tables)

    n_total = len(tables)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)

    train_tables = tables[:n_train]
    val_tables = tables[n_train:n_train + n_val]
    test_tables = tables[n_train + n_val:]

    os.makedirs(output_dir, exist_ok=True)

    for split_name, split_data in [("train", train_tables), ("val", val_tables), ("test", test_tables)]:
        split_instances = []
        for tbl in split_data:
            instances = generate_bio_tagged_tokens(tbl)
            split_instances.extend(instances)

        # Save raw split
        with open(os.path.join(output_dir, f"{split_name}_tables.json"), "w", encoding="utf-8") as f:
            json.dump(split_data, f, indent=2)

        # Save tokenized instances
        with open(os.path.join(output_dir, f"{split_name}_tokenized.json"), "w", encoding="utf-8") as f:
            json.dump(split_instances, f, indent=2)

    return {
        "train_tables": len(train_tables),
        "val_tables": len(val_tables),
        "test_tables": len(test_tables),
        "total_tables": n_total
    }

if __name__ == "__main__":
    res = create_dataset_splits()
    print("Dataset split completed:", res)
