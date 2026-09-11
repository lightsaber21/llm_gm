# PDF To Text Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a CLI script that extracts text from a PDF into `.txt` or `.md`.

**Architecture:** One Python script owns CLI parsing, PDF extraction, output formatting, and file writing. `PyMuPDF` does PDF reading; the script only wraps it with small validation and two output formats.

**Tech Stack:** Python 3, `PyMuPDF`.

## Global Constraints

- Use `PyMuPDF` for PDF extraction.
- Avoid OCR, table reconstruction, and custom layout parsing.
- Command shape: `python3 scripts/pdf_to_text.py input.pdf [output_path] --format txt`.
- Command shape: `python3 scripts/pdf_to_text.py input.pdf [output_path] --format md`.
- `--format` defaults to `txt`.
- Omitted output path writes beside the PDF with `.txt` or `.md`.
- TXT output uses `--- Page N ---` separators.
- Markdown output uses `# input` and `## Page N` headings.
- Fail on missing file, non-file input, unreadable PDF, or empty extraction.

---

### Task 1: PDF Extraction CLI

**Files:**
- Create: `requirements.txt`
- Create: `scripts/pdf_to_text.py`

**Interfaces:**
- Consumes: CLI args `pdf`, optional `output_path`, optional `--format {txt,md}`.
- Produces: `extract_pages(pdf_path: Path) -> list[str]`, `render_text(pages: list[str]) -> str`, `render_markdown(title: str, pages: list[str]) -> str`, and process exit code `0` on success.

- [ ] **Step 1: Add dependency file**

Create `requirements.txt`:

```text
PyMuPDF>=1.28
```

- [ ] **Step 2: Add CLI script**

Create `scripts/pdf_to_text.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    print("Missing dependency: install with `python3 -m pip install -r requirements.txt`", file=sys.stderr)
    raise SystemExit(1)


def extract_pages(pdf_path: Path) -> list[str]:
    if not pdf_path.exists():
        raise ValueError(f"Input does not exist: {pdf_path}")
    if not pdf_path.is_file():
        raise ValueError(f"Input is not a file: {pdf_path}")

    try:
        with pymupdf.open(pdf_path) as document:
            pages = [page.get_text().strip() for page in document]
    except Exception as exc:
        raise ValueError(f"Could not read PDF: {pdf_path}") from exc

    if not any(pages):
        raise ValueError(f"No text extracted from: {pdf_path}")
    return pages


def render_text(pages: list[str]) -> str:
    chunks = [f"--- Page {index} ---\n{text}" for index, text in enumerate(pages, start=1)]
    return "\n\n".join(chunks).strip() + "\n"


def render_markdown(title: str, pages: list[str]) -> str:
    chunks = [f"## Page {index}\n\n{text}" for index, text in enumerate(pages, start=1)]
    return f"# {title}\n\n" + "\n\n".join(chunks).strip() + "\n"


def default_output_path(pdf_path: Path, output_format: str) -> Path:
    return pdf_path.with_suffix(f".{output_format}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract PDF text into txt or md.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_path", type=Path, nargs="?")
    parser.add_argument("--format", choices=("txt", "md"), default="txt")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    pdf_path = args.pdf
    output_path = args.output_path or default_output_path(pdf_path, args.format)

    try:
        pages = extract_pages(pdf_path)
        output = render_markdown(pdf_path.stem, pages) if args.format == "md" else render_text(pages)
        output_path.write_text(output, encoding="utf-8")
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Compile-check script**

Run:

```bash
python3 -m py_compile scripts/pdf_to_text.py
```

Expected: exit code `0`.

- [ ] **Step 4: Install dependency when missing**

Run:

```bash
python3 -m pip install -r requirements.txt
```

Expected: `PyMuPDF` installed or already satisfied.

- [ ] **Step 5: Run TXT extraction**

Run:

```bash
python3 scripts/pdf_to_text.py data/mage_the_ascension_starter_guide.pdf --format txt
```

Expected: prints `data/mage_the_ascension_starter_guide.txt`.

- [ ] **Step 6: Run Markdown extraction**

Run:

```bash
python3 scripts/pdf_to_text.py data/mage_the_ascension_starter_guide.pdf --format md
```

Expected: prints `data/mage_the_ascension_starter_guide.md`.

- [ ] **Step 7: Inspect outputs**

Run:

```bash
head -5 data/mage_the_ascension_starter_guide.txt
head -5 data/mage_the_ascension_starter_guide.md
```

Expected: TXT starts with `--- Page 1 ---`; Markdown starts with `# mage_the_ascension_starter_guide`.

- [ ] **Step 8: Commit**

```bash
git add requirements.txt scripts/pdf_to_text.py docs/superpowers/plans/2026-09-11-pdf-to-text.md
git commit -m "feat: add pdf text extraction script"
```
