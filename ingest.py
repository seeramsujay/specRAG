import logging
import uuid
import chromadb
from langchain_text_splitters import MarkdownHeaderTextSplitter

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize ChromaDB Persistent Client and Collection
try:
    client = chromadb.PersistentClient(path="./vector_store")
    collection = client.get_or_create_collection(name="hardware_datasheets")
    logger.info(
        "Successfully connected to ChromaDB and initialized 'hardware_datasheets' collection."
    )
except Exception as e:
    logger.error("Failed to initialize ChromaDB client/collection: %s", e)
    raise


def ingest_markdown(markdown_text: str) -> None:
    """
    Ingestion pipeline:
    1. Splits a long Markdown string semantically using LangChain's MarkdownHeaderTextSplitter.
    2. Inserts resulting chunks into the hardware_datasheets ChromaDB collection.
    """
    logger.info("Starting ingestion pipeline...")
    if not markdown_text or not markdown_text.strip():
        logger.warning("Empty markdown text provided. Skipping ingestion.")
        return

    try:
        # Define headers to split on
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        # Initialize the splitter
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        logger.info("Splitting markdown content...")
        chunks = splitter.split_text(markdown_text)

        if not chunks:
            logger.warning("No chunks generated from split.")
            return

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            content = chunk.page_content.strip()
            if content:
                documents.append(content)
                metadatas.append(chunk.metadata)
                ids.append(str(uuid.uuid4()))

        if not documents:
            logger.warning(
                "No non-empty chunks found after splitting. Skipping ChromaDB insert."
            )
            return

        logger.info("Inserting %d chunks into collection...", len(documents))
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        logger.info("Successfully inserted %d chunks into ChromaDB.", len(documents))

    except Exception as e:
        logger.error("Error occurred during ingestion pipeline: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    # Sample run to verify the pipeline
    sample_markdown = """
# I2C Temperature Sensor TMP102

This datasheet describes the TMP102 temperature sensor.

## Electrical Specifications

- Absolute Maximum VIN is 3.3V
- Operating Temperature: -40C to 125C

### Absolute Maximum Ratings

Stresses above those listed under Absolute Maximum Ratings may cause permanent damage.

## Register Map

The device registers are described below.

### Temperature Register (0x00)

This is a read-only register containing the temperature value.

### Configuration Register (0x01)

This is a read/write register. Register 0x02 is Read-Only.
"""
    print("\n--- Running Sample Ingestion ---")
    ingest_markdown(sample_markdown)

    print("\n--- Verifying Ingested Chunks ---")
    try:
        # Retrieve all items in the collection to verify insertion
        count = collection.count()
        print(f"Total documents in collection: {count}")

        # Test query
        query_text = "What is the maximum VIN voltage?"
        print(f"Querying: '{query_text}'")
        results = collection.query(query_texts=[query_text], n_results=2)

        for i in range(len(results["ids"][0])):
            print(f"\nResult {i+1}:")
            print(f"ID: {results['ids'][0][i]}")
            print(f"Distance: {results['distances'][0][i]}")
            print(f"Metadata: {results['metadatas'][0][i]}")
            print(f"Content: {results['documents'][0][i]}")

    except Exception as e:
        print(f"Error during verification: {e}")
