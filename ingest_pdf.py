import sys
import logging
from pypdf import PdfReader
from ingest import ingest_markdown

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def ingest_pdf_file(pdf_path: str) -> None:
    """
    Reads a PDF file, extracts text page by page, formats each page with a markdown header,
    and passes the resulting markdown string to the ingest_markdown function.
    """
    logger.info("Opening PDF file: %s", pdf_path)
    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        logger.info("Total pages found: %d", num_pages)

        markdown_content = []
        for idx in range(num_pages):
            page = reader.pages[idx]
            page_text = page.extract_text()

            # Formulate a header for each page
            markdown_content.append(f"## Page {idx + 1}\n")
            if page_text and page_text.strip():
                markdown_content.append(page_text)
            else:
                markdown_content.append("*(No extractable text on this page)*")
            markdown_content.append("\n\n")

        full_markdown = "".join(markdown_content)
        logger.info("Extracted text successfully. Handing over to ingest_markdown...")

        ingest_markdown(full_markdown)
        logger.info("PDF ingestion complete.")

    except Exception as e:
        logger.error("Error occurred while ingesting PDF file: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Please provide the path to the PDF file as an argument.")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    ingest_pdf_file(pdf_file_path)
