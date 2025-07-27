# PDF Outline Extractor (Round 1A)

## Overview
This solution extracts a structured **outline** from PDF files, including:
- Document Title
- Headings (H1, H2, H3)
- Page numbers

The extracted outline is saved as a JSON file for each PDF in the required format.

## Approach
- The solution uses **font size-based heuristics** to identify headings.
- Headings are categorized as:
  - **H1** → Largest font size
  - **H2** → Second largest
  - **H3** → Third largest
- The **document title** is the first H1 heading encountered.

Example Output:
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## Libraries Used
- PyMuPDF (fitz)
- json, os, collections.Counter

## Docker Build & Run Instructions
### Build the Docker Image:
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

### Run the Container:
Linux/Mac:
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

Windows PowerShell:
```powershell
docker run --rm `
  -v "${PWD}/input:/app/input" `
  -v "${PWD}/output:/app/output" `
  --network none `
  pdf-outline-extractor:latest
```

## Expected Output
Each PDF in `/input` generates a JSON file in `/output`.

## Constraints
- Must run offline
- No GPU, CPU only
