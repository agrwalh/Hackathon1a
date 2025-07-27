# Filename: extract_outline.py

import fitz  # PyMuPDF
import json
import os
from collections import Counter

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    font_info = []
    headings = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    font_info.append(span['size'])

    # Heuristic: larger font sizes typically indicate headings
    common_sizes = Counter(font_info).most_common()
    if len(common_sizes) < 3:
        return None
    size_to_level = {
        common_sizes[0][0]: 'H1',
        common_sizes[1][0]: 'H2',
        common_sizes[2][0]: 'H3',
    }

    title = ""
    outline = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    size = span['size']
                    text = span['text'].strip()
                    if size in size_to_level and len(text) > 2:
                        level = size_to_level[size]
                        if not title and level == 'H1':
                            title = text
                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })

    return {
        "title": title or "Untitled Document",
        "outline": outline
    }

def process_all_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(input_dir, filename)
            result = extract_headings(filepath)
            if result:
                output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    process_all_pdfs(input_dir, output_dir)
