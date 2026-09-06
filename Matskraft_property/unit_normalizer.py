"""
Unit Parser and Normalizer for Material Properties.
Standardizes scientific units extracted from table headers and cell annotations.
"""

import re
from typing import Optional

UNIT_NORMALIZATION_MAP = {
    "g/cm3": "g/cm³",
    "g/cm^3": "g/cm³",
    "g cm-3": "g/cm³",
    "g cm^-3": "g/cm³",
    "mpa": "MPa",
    "gpa": "GPa",
    "k": "K",
    "deg c": "°C",
    "degc": "°C",
    "°c": "°C",
    "c": "°C",
    "mah/g": "mAh/g",
    "wh/kg": "Wh/kg",
    "v": "V",
    "mv": "mV",
    "hv": "HV",
    "hv30": "HV30",
    "pc/n": "pC/N",
    "uc/cm2": "µC/cm²",
    "µc/cm2": "µC/cm²",
    "s/cm": "S/cm",
    "w/mk": "W/m·K",
    "w/m-k": "W/m·K",
    "w/(mk)": "W/m·K",
    "uv/k": "µV/K",
    "µv/k": "µV/K",
    "uw/cmk2": "µW/cm·K²",
    "tesla": "T",
    "t": "T",
    "ma/cm2": "MA/cm²",
    "nm": "nm",
    "ev": "eV",
    "%": "%",
    "mpa m^0.5": "MPa·m^0.5",
    "10^-6 /k": "10⁻⁶/K",
    "tan delta": "dimensionless"
}

def extract_unit_from_text(text: str) -> Optional[str]:
    """Extracts unit inside parentheses or brackets, e.g. 'Yield Strength (MPa)' -> 'MPa'."""
    # Look for content in parentheses or square brackets
    match = re.search(r'[\(\[]([^\)\]]+)[\)\]]', text)
    if match:
        unit_raw = match.group(1).strip().lower()
        return normalize_unit(unit_raw)
    
    # Check if text ends with a known unit
    for k, v in UNIT_NORMALIZATION_MAP.items():
        if text.lower().endswith(k):
            return v

    return None

def normalize_unit(raw_unit: str) -> str:
    """Normalizes raw unit string into standard scientific representation."""
    if not raw_unit:
        return ""
    clean = raw_unit.strip().lower()
    clean = clean.replace("·", "").replace(" ", "").replace("*", "")
    
    if clean in UNIT_NORMALIZATION_MAP:
        return UNIT_NORMALIZATION_MAP[clean]

    for k, v in UNIT_NORMALIZATION_MAP.items():
        if k in clean:
            return v

    return raw_unit.strip()
