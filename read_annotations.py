#!/usr/bin/env python3
"""
Extract annotations (highlights, comments, sticky notes) from a PDF.

Usage:
    python read_annotations.py <path_to_pdf>
    python read_annotations.py ../main.pdf
    python read_annotations.py ../main.pdf --json

Requires: pymupdf (fitz)
    pip install pymupdf
"""

import sys
import json
import fitz  # pymupdf


def extract_annotations(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    annotations = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        for annot in page.annots() or []:
            info = annot.info
            annot_type = annot.type[1]  # e.g. 'Highlight', 'Text', 'FreeText', 'StrikeOut'

            highlighted_text = ""
            context_before = ""
            context_after = ""
            if annot_type in ("Highlight", "Underline", "StrikeOut", "Squiggly"):
                quads = annot.vertices
                if quads:
                    quad_count = len(quads) // 4
                    rects = []
                    for i in range(quad_count):
                        quad = quads[i * 4 : (i + 1) * 4]
                        rect = fitz.Quad(quad).rect
                        rects.append(rect)
                    for rect in rects:
                        highlighted_text += page.get_text("text", clip=rect)
                    highlighted_text = highlighted_text.strip()

                    # Extract surrounding context (5 words before and after)
                    if highlighted_text:
                        page_text = page.get_text("text")
                        pos = page_text.find(highlighted_text)
                        if pos >= 0:
                            before = page_text[:pos].split()
                            after = page_text[pos + len(highlighted_text):].split()
                            context_before = " ".join(before[-15:]) if before else ""
                            context_after = " ".join(after[:15]) if after else ""

            entry = {
                "page": page_num + 1,
                "type": annot_type,
                "comment": info.get("content", "").strip(),
                "highlighted_text": highlighted_text,
                "context_before": context_before,
                "context_after": context_after,
                "author": info.get("title", ""),
                "created": info.get("creationDate", ""),
            }

            # skip empty annotations
            if entry["comment"] or entry["highlighted_text"]:
                annotations.append(entry)

    doc.close()
    return annotations


def format_annotations(annotations: list[dict]) -> str:
    if not annotations:
        return "No annotations found in this PDF."

    lines = [f"Found {len(annotations)} annotation(s):\n"]
    for i, a in enumerate(annotations, 1):
        lines.append(f"--- Annotation {i} (Page {a['page']}, {a['type']}) ---")
        if a["highlighted_text"]:
            ctx = ""
            if a.get("context_before") or a.get("context_after"):
                ctx_b = f"...{a['context_before']} " if a.get("context_before") else ""
                ctx_a = f" {a['context_after']}..." if a.get("context_after") else ""
                ctx = f"\n  Context: {ctx_b}>>>{a['highlighted_text']}<<<{ctx_a}"
            lines.append(f"  Highlighted: \"{a['highlighted_text']}\"{ctx}")
        if a["comment"]:
            lines.append(f"  Comment: {a['comment']}")
        if a["author"]:
            lines.append(f"  Author: {a['author']}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_annotations.py <pdf_path> [--json]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    use_json = "--json" in sys.argv

    annotations = extract_annotations(pdf_path)

    if use_json:
        print(json.dumps(annotations, indent=2, ensure_ascii=False))
    else:
        print(format_annotations(annotations))
