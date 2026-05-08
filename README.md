# PDF Annotation Skill for Claude Code

Extract highlights, comments, sticky notes, and strikeouts from annotated PDFs — directly inside Claude Code.

## What it does

When you annotate a PDF (in Preview, PDF Expert, Acrobat, etc.) and ask Claude Code to read your annotations, this skill extracts them with full context and treats each comment as a revision instruction.

## Install

```bash
npx skills add xisen-w/PDF-annotation-skill
```

## Usage

```
/read-annotated-pdf path/to/your-file.pdf
```

Or just ask naturally:

- "Read my annotations on main_v2.pdf"
- "看看我在 paper.pdf 上的批注"
- "Check the comments I left on thesis.pdf"

## Sample Output

```
Found 3 annotation(s):

--- Annotation 1 (Page 2, Highlight) ---
  Highlighted: "The frontier is no longer chosen. It is emergent."
  Context: ...policy text alone where the boundary will >>>The frontier is no longer chosen. It is emergent.<<< We cannot predict from...
  Comment: Make it one academic sentence
  Author: wangxiang

--- Annotation 2 (Page 4, Highlight) ---
  Highlighted: "Table 1: Experimental dimensions."
  Context: >>>Table 1: Experimental dimensions.<<< Each RQ isolates one axis while controlling the others...
  Comment: Put the table even earlier for better 排版
  Author: wangxiang

--- Annotation 3 (Page 8, Highlight) ---
  Highlighted: "(category deny list) shifts all six models to high security..."
  Comment: make it more concise!, like 1/2 to 2/3
  Author: wangxiang
```

After presenting annotations, Claude will ask whether to apply the changes to your source files.

## Supported Annotation Types

| Type | Description |
|------|-------------|
| Highlight | Selected text with optional comment |
| Text | Sticky note (comment pinned to a location) |
| FreeText | Inline text annotation |
| StrikeOut | Struck-through text with optional comment |
| Underline | Underlined text with optional comment |
| Squiggly | Squiggly-underlined text |

## How Comments Are Interpreted

| Comment | Action |
|---------|--------|
| "rewrite" / "改" | Rewrite the highlighted section |
| "delete" / "删" | Remove the content |
| A question | Answer it and propose an edit |
| No comment (highlight only) | Flag for clarification |

## Requirements

- Python 3.8+
- `pymupdf` (installed automatically if missing)

```bash
pip install pymupdf
```

## Tip

Never recompile a PDF over an annotated file — LaTeX will overwrite the annotations. Always compile to a versioned filename (e.g., `main_v2.pdf`).
