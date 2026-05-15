#!/usr/bin/env python3
"""Convert a Markdown file to a simple PDF using ReportLab."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)


INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to PDF using ReportLab."
    )
    parser.add_argument("input", type=Path, help="Markdown input file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="PDF output file. Defaults to the input filename with .pdf extension.",
    )
    return parser.parse_args()


def inline_markup(text: str) -> str:
    """Convert a small Markdown inline subset to ReportLab paragraph markup."""
    text = html.escape(text)
    text = INLINE_CODE_RE.sub(r'<font name="Courier">\1</font>', text)
    text = BOLD_RE.sub(r"<b>\1</b>", text)
    text = ITALIC_RE.sub(r"<i>\1</i>", text)
    return text


def flush_paragraph(story: list, lines: list[str], style: ParagraphStyle) -> None:
    if not lines:
        return
    story.append(Paragraph(inline_markup(" ".join(lines)), style))
    story.append(Spacer(1, 0.08 * inch))
    lines.clear()


def flush_list(
    story: list,
    items: list[str],
    style: ParagraphStyle,
    ordered: bool,
) -> None:
    if not items:
        return
    flowables = [
        ListItem(Paragraph(inline_markup(item), style), leftIndent=12) for item in items
    ]
    story.append(
        ListFlowable(
            flowables,
            bulletType="1" if ordered else "bullet",
            leftIndent=18,
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    items.clear()


def build_story(markdown_text: str) -> list:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=10,
            leftIndent=12,
            rightIndent=12,
            backColor=colors.whitesmoke,
            borderColor=colors.lightgrey,
            borderWidth=0.5,
            borderPadding=6,
            spaceAfter=8,
        )
    )

    story: list = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []
    list_ordered = False
    in_code_block = False
    code_lines: list[str] = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph(story, paragraph_lines, styles["BodyText"])
            flush_list(story, list_items, styles["BodyText"], list_ordered)
            if in_code_block:
                story.append(Preformatted("\n".join(code_lines), styles["CodeBlock"]))
                story.append(Spacer(1, 0.08 * inch))
                code_lines.clear()
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph(story, paragraph_lines, styles["BodyText"])
            flush_list(story, list_items, styles["BodyText"], list_ordered)
            continue

        if stripped in {"---", "***", "___"}:
            flush_paragraph(story, paragraph_lines, styles["BodyText"])
            flush_list(story, list_items, styles["BodyText"], list_ordered)
            story.append(Spacer(1, 0.18 * inch))
            continue

        if stripped == "\\pagebreak":
            flush_paragraph(story, paragraph_lines, styles["BodyText"])
            flush_list(story, list_items, styles["BodyText"], list_ordered)
            story.append(PageBreak())
            continue

        heading_match = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading_match:
            flush_paragraph(story, paragraph_lines, styles["BodyText"])
            flush_list(story, list_items, styles["BodyText"], list_ordered)
            level = len(heading_match.group(1))
            style_name = {1: "Title", 2: "Heading2", 3: "Heading3"}[level]
            story.append(Paragraph(inline_markup(heading_match.group(2)), styles[style_name]))
            story.append(Spacer(1, 0.08 * inch))
            continue

        unordered_match = re.match(r"^[-*+]\s+(.+)$", stripped)
        ordered_match = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if unordered_match or ordered_match:
            flush_paragraph(story, paragraph_lines, styles["BodyText"])
            ordered = bool(ordered_match)
            if list_items and ordered != list_ordered:
                flush_list(story, list_items, styles["BodyText"], list_ordered)
            list_ordered = ordered
            list_items.append((ordered_match or unordered_match).group(1))
            continue

        flush_list(story, list_items, styles["BodyText"], list_ordered)
        paragraph_lines.append(stripped)

    flush_paragraph(story, paragraph_lines, styles["BodyText"])
    flush_list(story, list_items, styles["BodyText"], list_ordered)
    if in_code_block and code_lines:
        story.append(Preformatted("\n".join(code_lines), styles["CodeBlock"]))

    return story


def convert_markdown_to_pdf(input_path: Path, output_path: Path) -> None:
    markdown_text = input_path.read_text(encoding="utf-8")
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=input_path.stem,
    )
    document.build(build_story(markdown_text))


def main() -> int:
    args = parse_args()
    input_path = args.input
    output_path = args.output or input_path.with_suffix(".pdf")

    if not input_path.exists():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 1
    if input_path.is_dir():
        print(f"error: input path is a directory: {input_path}", file=sys.stderr)
        return 1
    if output_path.suffix.lower() != ".pdf":
        print(f"error: output file must end with .pdf: {output_path}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    convert_markdown_to_pdf(input_path, output_path)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
