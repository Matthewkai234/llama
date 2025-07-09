# utils.py

"""
Utility to convert CSV content into paragraph text blocks.
"""

import pandas as pd
import re


def csv_to_paragraphs(file_path: str) -> list[str]:
    """
    Reads a CSV file and converts each row into a single paragraph.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        list[str]: Cleaned text paragraphs.
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='windows-1256')

    paragraphs = []
    for _, row in df.iterrows():
        text = " - ".join([f"{col.strip()}: {str(row[col])}" for col in df.columns])
        clean_text = re.sub(r'\s+', ' ', text.strip())
        paragraphs.append(clean_text)

    return paragraphs
