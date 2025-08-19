# # utils.py

"""
Utility functions for processing CSV content into text blocks.
"""

import pandas as pd
import re


def csv_to_paragraphs(file_path: str) -> list[str]:
    """
    Converts each row of a CSV file into a single cleaned paragraph string.

    Each row is transformed into the format:
        "column1: value1 - column2: value2 - ..."

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list[str]: A list of paragraph strings, one for each row in the CSV,
                   with extra whitespace removed and columns joined.

    Raises:
        FileNotFoundError: If the CSV file does not exist at the given path.
        UnicodeDecodeError: If the file cannot be decoded in UTF-8 or Windows-1256.
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
