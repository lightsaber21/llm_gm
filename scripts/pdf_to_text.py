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
