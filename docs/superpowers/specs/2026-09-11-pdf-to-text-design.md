# PDF To Text Script Design

## Goal

Add a small script that extracts text from a PDF and writes a UTF-8 text or Markdown file for LLM reading.

## Approach

Use `PyMuPDF` (`fitz`) because it is fast, reliable for ordinary PDFs, and keeps the script small. Avoid OCR, table reconstruction, and custom layout parsing.

## Interface

Command:

```bash
python3 scripts/pdf_to_text.py input.pdf [output_path] --format txt
python3 scripts/pdf_to_text.py input.pdf [output_path] --format md
```

`--format` defaults to `txt`.

If `output_path` is omitted, the script writes beside the PDF using the same stem and an extension matching the selected format: `.txt` or `.md`.

## Output Format

Plain text uses page separators:

```text
--- Page 1 ---
...
```

Markdown uses document and page headings:

```md
# input

## Page 1

...
```

Plain text remains the simplest default. Markdown is available when page structure is useful for LLM prompts or notes.

## Error Handling

Fail with a concise message when the input path does not exist, is not a file, cannot be opened as a PDF, or extracts no text.

## Testing

Run the script against `data/mage_the_ascension_starter_guide.pdf` in both `txt` and `md` modes. Confirm each output file exists and contains page-marked text.
