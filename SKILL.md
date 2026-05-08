---
name: read-annotated-pdf
description: Extract and display annotations (highlights, comments, sticky notes, strikeouts) from a PDF file. Use when the user asks to read annotations, check PDF comments, review highlights, or says "看看我的批注".
argument-hint: <path-to-pdf>
allowed-tools: Bash(python3 *)
---

Extract annotations from the given PDF using the bundled script.

## Instructions

1. Run the extraction script on the provided PDF path:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/read_annotations.py $ARGUMENTS
   ```

2. If `pymupdf` is not installed, install it first:
   ```bash
   pip install pymupdf
   ```

3. Parse the output. Each annotation has:
   - **page**: page number
   - **type**: Highlight, Text (sticky note), FreeText, StrikeOut, Underline, Squiggly
   - **highlighted_text**: the text that was highlighted/marked
   - **comment**: the user's written comment
   - **context_before / context_after**: surrounding text for locating the annotation

4. Group annotations by page and present them clearly to the user.

5. For each annotation with a comment, treat it as a revision instruction:
   - "rewrite" or "改" → rewrite that section
   - "delete" or "删" → remove that content
   - A question → answer it and propose an edit
   - Just a highlight with no comment → flag it for the user to clarify

6. After presenting all annotations, ask: "Should I apply these changes?" / "要我按这些批注改吗？"

## Important

- Never recompile a PDF over the annotated file — annotations are stored in the PDF and will be lost. Always compile to a new filename or versioned name.
- When applying changes, work on the `.tex` source, not the PDF.
