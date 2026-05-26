#!/usr/bin/env python3
"""
clean_markdown.py — Phase 1.5: Markdown Sanitizer
===================================================
Reads raw Markdown files produced by Azure AI Document Intelligence,
strips out page-level artifacts (HTML comments, legal footers, logo
figures), merges tables that were split across PDF page boundaries,
and writes clean files ready for vector-database chunking.

Usage:
    python clean_markdown.py                         # default dirs
    python clean_markdown.py --input raw/ --output clean/

Input:  raw_markdown/   (or --input)
Output: clean_markdown/ (or --output)

Constraint: NO technical data is altered, summarized, or reworded.
Only extraction artifacts are removed and split structures reunited.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from markdownify import markdownify as md


# ═══════════════════════════════════════════════════════════════════════
# 1.  ARTIFACT PURGING — RegEx patterns for page-level garbage
# ═══════════════════════════════════════════════════════════════════════

# HTML comments injected by Document Intelligence
#   <!-- PageHeader="..." -->   <!-- PageFooter="..." -->
#   <!-- PageBreak -->          <!-- PageNumber="..." -->
#   <!-- ========== PART 2 ... ========== -->  (our own merge marker)
RE_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)

# ALL <figure> blocks — Azure extracts jumbled, contextless text from
# block diagrams, pinout images, and logos.  None of it is useful for
# RAG retrieval; it pollutes the context window and causes hallucinations.
RE_FIGURE_BLOCK = re.compile(
    r"<figure>.*?</figure>",
    re.DOTALL,
)

# Table of Contents section — starts at ## TABLE OF CONTENTS and runs
# until the next ## header.  The ToC is just page numbers and section
# names that duplicate the real headers, adding zero retrieval value.
RE_TABLE_OF_CONTENTS = re.compile(
    r"^#{1,6}\s+TABLE OF CONTENTS\s*\n"
    r"(.*?)"
    r"(?=^#{1,6}\s+(?!TABLE OF CONTENTS)|\Z)",
    re.DOTALL | re.MULTILINE | re.IGNORECASE,
)

# ═══════════════════════════════════════════════════════════════════════
# 2.  FOOTER / DISCLAIMER REMOVAL
# ═══════════════════════════════════════════════════════════════════════

# Common Analog Devices / semiconductor vendor legal boilerplate
FOOTER_PATTERNS = [
    # Full ADI disclaimer (may span multiple lines)
    re.compile(
        r"Information furnished by Analog Devices is believed to be "
        r"accurate.*?(?:respective owners\.|All rights reserved\.)",
        re.DOTALL | re.IGNORECASE,
    ),
    # Short footer lines
    re.compile(r"^\s*www\.analog\.com\s*$", re.MULTILINE),
    re.compile(r"^\s*analog\.com\s*$", re.MULTILINE),
    # Copyright lines
    re.compile(
        r"^\s*@?\s*©?\s*\d{4}\s+Analog Devices.*$",
        re.MULTILINE | re.IGNORECASE,
    ),
    # Phone / fax lines that leak in
    re.compile(
        r"^\s*(?:Tel|Fax):\s*[\d.\-]+\s*$", re.MULTILINE
    ),
    # Standalone "DOCUMENT FEEDBACK" / "TECHNICAL SUPPORT" lines
    re.compile(
        r"^\s*(?:DOCUMENT FEEDBACK|TECHNICAL SUPPORT)\s*$",
        re.MULTILINE,
    ),
    # ADI address line
    re.compile(
        r"^\s*One Technology Way.*Norwood.*$",
        re.MULTILINE | re.IGNORECASE,
    ),
]


# ═══════════════════════════════════════════════════════════════════════
# 3.  TABLE MERGING
# ═══════════════════════════════════════════════════════════════════════

def _columns_of_table(table_html: str) -> int:
    """Count columns by looking at the first <tr>."""
    first_row = re.search(r"<tr>(.*?)</tr>", table_html, re.DOTALL)
    if not first_row:
        return 0
    return len(re.findall(r"<t[dh]>", first_row.group(1)))


def _has_header_row(table_html: str) -> bool:
    """Check if the table starts with <th> cells."""
    first_row = re.search(r"<tr>(.*?)</tr>", table_html, re.DOTALL)
    if not first_row:
        return False
    return "<th>" in first_row.group(1)


def _caption_of(table_html: str) -> str | None:
    """Extract <caption> text if present."""
    m = re.search(r"<caption>(.*?)</caption>", table_html, re.DOTALL)
    return m.group(1).strip() if m else None


def _extract_rows(table_html: str, skip_header: bool = False) -> str:
    """Return all <tr>...</tr> blocks, optionally skipping the first."""
    rows = re.findall(r"<tr>.*?</tr>", table_html, re.DOTALL)
    if skip_header and rows:
        rows = rows[1:]
    return "\n".join(rows)


def merge_split_tables(text: str) -> tuple[str, int]:
    """
    Detect adjacent HTML tables separated only by whitespace /
    page artifacts and merge them when they share the same column
    count and (if present) the same caption.

    Returns the cleaned text and the number of merges performed.
    """
    merge_count = 0

    # Pattern: </table> ... <table> with only whitespace between them
    # (artifacts will already have been stripped by this point).
    split_pat = re.compile(
        r"</table>"         # end of table A
        r"\s*"              # only whitespace
        r"<table>",         # start of table B
        re.DOTALL,
    )

    # Use an offset to avoid re-matching the same boundary.
    search_pos = 0

    while True:
        m = split_pat.search(text, search_pos)
        if not m:
            break

        # Find the full extent of table A and table B.
        # Walk backwards from m.start() to find the opening <table> of A.
        a_end = m.start() + len("</table>")
        a_open = text.rfind("<table>", 0, m.start())
        if a_open == -1:
            search_pos = m.end()
            continue

        # Walk forward from m.end() to find the closing </table> of B.
        b_open = m.end() - len("<table>")
        b_close_idx = text.find("</table>", m.end())
        if b_close_idx == -1:
            search_pos = m.end()
            continue

        table_a = text[a_open:a_end]
        table_b = text[b_open:b_close_idx + len("</table>")]

        cols_a = _columns_of_table(table_a)
        cols_b = _columns_of_table(table_b)

        cap_a = _caption_of(table_a)
        cap_b = _caption_of(table_b)

        # Merge conditions:
        #   - Same column count, OR table B has no header (continuation)
        #   - Captions match or one is missing
        same_cols = (cols_a == cols_b) or (cols_a > 0 and not _has_header_row(table_b))
        caps_compatible = (
            cap_a is None or cap_b is None or cap_a == cap_b
        )

        if same_cols and caps_compatible:
            # Take rows from B (skip its header if it duplicates A's).
            skip = _has_header_row(table_b) and _has_header_row(table_a) and cols_a == cols_b
            new_rows = _extract_rows(table_b, skip_header=skip)

            # Splice: insert B's rows before A's closing </table>,
            # then remove table B entirely.
            merged = table_a.replace("</table>", f"\n{new_rows}\n</table>")
            text = text[:a_open] + merged + text[b_close_idx + len("</table>"):]
            merge_count += 1
            # Don't advance search_pos — the merged table may adjoin
            # yet another table that should also be merged.
        else:
            # Not mergeable — skip past this boundary.
            search_pos = m.end()

    return text, merge_count


# ═══════════════════════════════════════════════════════════════════════
# 4.  HEADER FORMATTING
# ═══════════════════════════════════════════════════════════════════════

def fix_header_spacing(text: str) -> str:
    """
    Ensure every Markdown header (# … ######) is preceded and followed
    by exactly one blank line, so downstream chunking tools can split
    on headers reliably.
    """
    # Header followed by non-blank line → insert blank line after.
    text = re.sub(
        r"(^#{1,6}\s+.+)(\n)(?=\S)",
        r"\1\n\n",
        text,
        flags=re.MULTILINE,
    )
    # Non-blank line immediately before a header → insert blank line.
    text = re.sub(
        r"(\S)(\n)(#{1,6}\s+)",
        r"\1\n\n\3",
        text,
        flags=re.MULTILINE,
    )
    return text


# ═══════════════════════════════════════════════════════════════════════
# 5.  COSMETIC CLEANUP
# ═══════════════════════════════════════════════════════════════════════

def collapse_blank_lines(text: str) -> str:
    """Replace runs of 3+ blank lines with exactly 2."""
    return re.sub(r"\n{4,}", "\n\n\n", text)


def purge_revision_history(text: str) -> tuple[str, int]:
    """
    Locate the REVISION HISTORY section via string slicing (.find())
    and remove all text below it until the start of the next major
    Markdown header or end of file.
    """
    removed = 0
    lower_text = text.lower()
    
    # Try searching for common header levels of revision history
    for target in ["## revision history", "# revision history", "### revision history"]:
        idx = lower_text.find(target)
        if idx != -1:
            # Found the revision history section!
            search_start = idx + len(target)
            # Find the next header starting with '#' on a new line
            next_header_idx = text.find("\n#", search_start)
            if next_header_idx != -1:
                # Remove everything between the start of the Revision History header
                # and the next header (keeping the newline and the next header)
                text = text[:idx] + text[next_header_idx:]
            else:
                # It is the last section in the document, slice until the end
                text = text[:idx]
            removed = 1
            break
            
    return text, removed


def convert_html_tables_to_markdown(text: str) -> str:
    """
    Find all HTML table blocks (<table>...</table>) and convert them
    to clean Markdown pipe-and-dash tables using markdownify,
    reversing any markdown escaping of underscores/asterisks to prevent
    data alteration.
    """
    table_pat = re.compile(r"<table>.*?</table>", re.DOTALL)
    
    def replace_table(match):
        table_html = match.group(0)
        # Convert table HTML to Markdown table
        table_md = md(table_html)
        # Unescape markdownify-escaped characters that are part of register/pin names
        table_md_clean = table_md.replace(r"\_", "_").replace(r"\*", "*")
        return "\n\n" + table_md_clean.strip() + "\n\n"
        
    return table_pat.sub(replace_table, text)


# ═══════════════════════════════════════════════════════════════════════
# 6.  MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════

def clean_file(raw_text: str) -> tuple[str, dict]:
    """
    Run the full sanitization pipeline on a single document.

    Returns:
        (cleaned_text, stats_dict)
    """
    stats = {
        "html_comments_removed": 0,
        "figures_removed": 0,
        "toc_sections_removed": 0,
        "revision_history_removed": 0,
        "footers_removed": 0,
        "tables_merged": 0,
    }

    text = raw_text

    # ── Step 1: Count & remove HTML comments ──────────────────────────
    stats["html_comments_removed"] = len(RE_HTML_COMMENT.findall(text))
    text = RE_HTML_COMMENT.sub("", text)

    # ── Step 2: Remove ALL <figure> blocks ─────────────────────────────
    stats["figures_removed"] = len(RE_FIGURE_BLOCK.findall(text))
    text = RE_FIGURE_BLOCK.sub("", text)

    # ── Step 2b: Remove TABLE OF CONTENTS sections ────────────────────
    stats["toc_sections_removed"] = len(RE_TABLE_OF_CONTENTS.findall(text))
    text = RE_TABLE_OF_CONTENTS.sub("", text)

    # ── Step 2c: Remove REVISION HISTORY sections ─────────────────────
    text, stats["revision_history_removed"] = purge_revision_history(text)

    # ── Step 3: Remove legal disclaimers / footers ────────────────────
    for pat in FOOTER_PATTERNS:
        hits = len(pat.findall(text))
        stats["footers_removed"] += hits
        text = pat.sub("", text)

    # ── Step 4: Merge split tables ────────────────────────────────────
    text, stats["tables_merged"] = merge_split_tables(text)

    # ── Step 4b: Convert HTML tables to Markdown pipe-and-dash format ──
    text = convert_html_tables_to_markdown(text)

    # ── Step 5: Fix header spacing ────────────────────────────────────
    text = fix_header_spacing(text)

    # ── Step 6: Collapse excessive blank lines ────────────────────────
    text = collapse_blank_lines(text)

    # Trim leading/trailing whitespace
    text = text.strip() + "\n"

    return text, stats


def process_directory(input_dir: Path, output_dir: Path) -> None:
    """Process every .md file in input_dir → output_dir."""
    md_files = sorted(input_dir.glob("*.md"))

    if not md_files:
        print(f"⚠️  No .md files found in {input_dir}/")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'─' * 60}")
    print(f"  clean_markdown.py — Sanitization Pipeline")
    print(f"  Input:  {input_dir.resolve()}")
    print(f"  Output: {output_dir.resolve()}")
    print(f"  Files:  {len(md_files)}")
    print(f"{'─' * 60}\n")

    total_stats = {
        "html_comments_removed": 0,
        "figures_removed": 0,
        "toc_sections_removed": 0,
        "revision_history_removed": 0,
        "footers_removed": 0,
        "tables_merged": 0,
    }

    for md_file in md_files:
        raw_text = md_file.read_text(encoding="utf-8")
        cleaned, stats = clean_file(raw_text)

        # Append '_clean' suffix to distinguish processed files
        out_name = md_file.stem + "_clean.md"
        out_path = output_dir / out_name
        out_path.write_text(cleaned, encoding="utf-8")

        # Per-file report
        raw_kb = len(raw_text.encode("utf-8")) / 1024
        clean_kb = len(cleaned.encode("utf-8")) / 1024
        reduction = (1 - clean_kb / raw_kb) * 100 if raw_kb else 0

        print(f"  📄 {md_file.name}")
        print(f"     Size: {raw_kb:.1f} KB → {clean_kb:.1f} KB ({reduction:.0f}% reduction)")
        print(f"     HTML comments removed:  {stats['html_comments_removed']}")
        print(f"     Figure blocks removed:  {stats['figures_removed']}")
        print(f"     ToC sections removed:   {stats['toc_sections_removed']}")
        print(f"     Revision History sections removed: {stats['revision_history_removed']}")
        print(f"     Footers removed:        {stats['footers_removed']}")
        print(f"     Tables merged:          {stats['tables_merged']}")
        print()

        for key in total_stats:
            total_stats[key] += stats[key]

    # Summary
    print(f"{'─' * 60}")
    print(f"  ✅ TOTAL SUMMARY ({len(md_files)} files)")
    print(f"     HTML comments removed:  {total_stats['html_comments_removed']}")
    print(f"     Figure blocks removed:  {total_stats['figures_removed']}")
    print(f"     ToC sections removed:   {total_stats['toc_sections_removed']}")
    print(f"     Revision History sections removed: {total_stats['revision_history_removed']}")
    print(f"     Footers removed:        {total_stats['footers_removed']}")
    print(f"     Tables merged:          {total_stats['tables_merged']}")
    print(f"{'─' * 60}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sanitize raw Azure Document Intelligence Markdown for RAG ingestion.",
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        default=Path("raw_markdown"),
        help="Directory containing raw .md files (default: raw_markdown/)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("clean_datasheets"),
        help="Directory for cleaned output (default: clean_datasheets/)",
    )
    args = parser.parse_args()

    if not args.input.is_dir():
        print(f"❌ Input directory not found: {args.input}")
        print(f"   Create it and place your raw .md files inside.")
        sys.exit(1)

    process_directory(args.input, args.output)


if __name__ == "__main__":
    main()
