# PDF To Text Script Design

## Goal

Add a small script that extracts text from a PDF and writes a UTF-8 text file for LLM reading.

## Approach

Use `PyMuPDF` (`fitz`) because it is fast, reliable for ordinary PDFs, and keeps the script small. Avoid OCR, Markdown conversion, table reconstruction, and custom layout parsing.

## Interface

Command:

```bash
python3 scripts/pdf_to_text.py input.pdf [output.txt]
```

If `output.txt` is omitted, the script writes beside the PDF using the same stem and `.txt`.

## Output Format

Plain text, with page separators:

```text
--- Page 1 ---
...
```

Plain text is the most LLM-friendly default for this use case. Markdown can come later if headings or tables become important.

## Error Handling

Fail with a concise message when the input path does not exist, is not a file, cannot be opened as a PDF, or extracts no text.

## Testing

Run the script against `data/mage_the_ascension_starter_guide.pdf` and confirm the output file exists and contains page-marked text.
