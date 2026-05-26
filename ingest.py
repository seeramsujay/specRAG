#!/usr/bin/env python3
"""
ingest.py — Phase 1: Datasheet PDF → Markdown Extraction
=========================================================
Uses Azure AI Document Intelligence (Layout Model) to convert complex
hardware datasheets into structurally-faithful Markdown files.

This script automatically splits large PDFs into smaller page batches to
work around the Azure F0 (Free Tier) 2-page limit and the 4MB payload limit.
It also includes robust retries with exponential backoff for HTTP 429
rate limiting.

Usage:
    python ingest.py input_datasheet.pdf [output.md] --chunk-size 2
"""

import argparse
import os
import sys
import time
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load environment variables from .env (if present)
# ---------------------------------------------------------------------------
load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")


def validate_config() -> None:
    """Ensure the required Azure credentials are available."""
    missing = []
    if not AZURE_ENDPOINT:
        missing.append("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not AZURE_KEY:
        missing.append("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if missing:
        print(
            "❌ Missing required environment variable(s):\n"
            + "\n".join(f"   • {var}" for var in missing)
        )
        print(
            "\nSet them in a .env file or export them in your shell. "
            "See .env.example for reference."
        )
        sys.exit(1)


def extract_pdf_chunk(client, AnalyzeDocumentRequest, chunk_bytes: bytes, start_page: int, end_page: int) -> str:
    """Send a PDF chunk to the Azure API and handle rate limits with backoff."""
    from azure.core.exceptions import HttpResponseError

    max_retries = 8
    backoff = 3.0

    for attempt in range(max_retries):
        try:
            poller = client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=AnalyzeDocumentRequest(bytes_source=chunk_bytes),
                output_content_format="markdown",
            )
            result = poller.result()
            return result.content
        except HttpResponseError as e:
            is_rate_limit = (
                e.status_code == 429
                or "rate limit" in str(e).lower()
                or "too many requests" in str(e).lower()
                or "RequestRateTooLarge" in str(e)
            )
            if is_rate_limit and attempt < max_retries - 1:
                # Read Retry-After header if present, otherwise use backoff
                retry_after = e.headers.get("Retry-After")
                sleep_time = float(retry_after) if retry_after and retry_after.replace('.', '', 1).isdigit() else backoff
                print(f"   ⚠️ Rate limit hit (429) on pages {start_page}-{end_page}. Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                backoff *= 1.8
            else:
                print(f"❌ API error processing pages {start_page}-{end_page}: {e}")
                raise e
    raise RuntimeError(f"Failed to process pages {start_page}-{end_page} after {max_retries} attempts.")


def extract_pdf_to_markdown(pdf_path: Path, chunk_size: int, delay: float) -> str:
    """
    Read PDF and send to Azure Document Intelligence in chunks.
    """
    # Late imports for clean dependency reporting
    try:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
        from azure.core.credentials import AzureKeyCredential
        from pypdf import PdfReader, PdfWriter
    except ImportError as e:
        print(
            f"❌ Required packages not found ({e}). Install them with:\n"
            "   pip install azure-ai-documentintelligence azure-core pypdf"
        )
        sys.exit(1)

    # --- 1. Initialize the client ----------------------------------------
    client = DocumentIntelligenceClient(
        endpoint=AZURE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_KEY),
    )

    # --- 2. Open PDF and check pages -------------------------------------
    print(f"📄 Opening PDF: {pdf_path}")
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"   Total Pages: {total_pages}")

    # Determine batch processing parameters
    if chunk_size <= 0:
        chunk_size = total_pages
    
    chunks = []
    for i in range(0, total_pages, chunk_size):
        chunks.append((i + 1, min(i + chunk_size, total_pages)))

    print(f"   Processing mode: Split into {len(chunks)} batch(es) (chunk size: {chunk_size} pages)")

    markdown_parts = []

    # --- 3. Process batches sequentially ---------------------------------
    for idx, (start_page, end_page) in enumerate(chunks):
        print(f"🔍 Batch {idx + 1}/{len(chunks)}: Pages {start_page} to {end_page}...")
        
        # Slice pages out into a memory buffer
        writer = PdfWriter()
        for p in range(start_page - 1, end_page):
            writer.add_page(reader.pages[p])
            
        chunk_stream = BytesIO()
        writer.write(chunk_stream)
        chunk_bytes = chunk_stream.getvalue()

        # Send chunk
        content = extract_pdf_chunk(client, AnalyzeDocumentRequest, chunk_bytes, start_page, end_page)
        markdown_parts.append(content)
        
        # Optional delay to stay under F0 rate limits (15 TPM = 4s delay)
        if idx < len(chunks) - 1 and delay > 0:
            time.sleep(delay)

    print("✅ All batches analyzed successfully.")

    # Combine all pieces with clean separation
    merged_markdown = "\n\n<!-- PageBreak -->\n\n".join(markdown_parts)
    return merged_markdown


def main() -> None:
    """CLI entry-point."""
    parser = argparse.ArgumentParser(
        description="Ingest complex PDF datasheets to Markdown using Azure Document Intelligence."
    )
    parser.add_argument("input_pdf", type=Path, help="Path to local input PDF file.")
    parser.add_argument("output_md", nargs="?", type=Path, default=None, help="Path to output markdown file.")
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=2,
        help="Number of pages per Azure request. Set to 2 for F0 Free Tier (default), or 0 to send full file."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=4.0,
        help="Time (seconds) to wait between requests to prevent rate limit triggers (default: 4.0)."
    )

    args = parser.parse_args()

    # Pre-flight checks
    if not args.input_pdf.exists():
        print(f"❌ Input file not found: {args.input_pdf}")
        sys.exit(1)

    if not args.input_pdf.suffix.lower() == ".pdf":
        print(f"⚠️  Warning: '{args.input_pdf.name}' does not have a .pdf extension.")

    validate_config()

    output_path = args.output_md
    if not output_path:
        output_path = args.input_pdf.with_suffix(".md")

    # Run extraction
    try:
        markdown_content = extract_pdf_to_markdown(args.input_pdf, args.chunk_size, args.delay)
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        sys.exit(1)

    # Save output
    output_path.write_text(markdown_content, encoding="utf-8")
    print(f"💾 Complete Markdown saved to: {output_path}")
    print(f"   Final size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
