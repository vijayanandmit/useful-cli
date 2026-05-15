# Markdown PDF Writer

Convert a Markdown file into a PDF with a small Python script that uses
ReportLab.

## Install

```bash
pip install reportlab
```

## Usage

Convert a Markdown file and choose the PDF output path:

```bash
python md_to_pdf.py input.md output.pdf
```

Or omit the output path to create a PDF next to the input file:

```bash
python md_to_pdf.py input.md
```

For example:

```bash
python md_to_pdf.py notes.md
```

This creates `notes.pdf`.

## Supported Markdown

The script supports a practical subset of Markdown:

- headings: `#`, `##`, `###`
- paragraphs
- unordered lists with `-`, `*`, or `+`
- ordered lists such as `1. item`
- fenced code blocks with triple backticks
- inline code with backticks
- bold text with `**bold**`
- italic text with `*italic*`
- horizontal rules with `---`, `***`, or `___`
- page breaks with `\pagebreak`

This is intended as a lightweight CLI utility. For complex Markdown features
such as tables, images, nested lists, footnotes, or full GitHub-flavored
Markdown rendering, use a dedicated Markdown publishing tool.
