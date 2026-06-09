import logging
import chromadb

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
        "Successfully connected to ChromaDB 'hardware_datasheets' collection for RAG querying."
    )
except Exception as e:
    logger.error("Failed to connect to ChromaDB collection: %s", e)
    collection = None


def retrieve_context(component_name: str, code_snippet: str = "") -> str:
    """
    Retrieves relevant datasheet context for the given hardware component
    by querying the ChromaDB database.

    Combines component_name and code_snippet as the search query.
    Returns the top 3 matches formatted with their section metadata headers.
    """
    logger.info("Retrieving live database context for component: %s", component_name)

    if collection is None:
        return f"Error: Database collection not initialized. Cannot retrieve context for {component_name}."

    # Build the query string using both the component name and the code snippet
    query_terms = [component_name]
    if code_snippet and code_snippet.strip():
        query_terms.append(code_snippet.strip())
    query_string = " ".join(query_terms)

    try:
        # Query ChromaDB collection
        results = collection.query(query_texts=[query_string], n_results=3)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not documents:
            return f"No context found in database for component '{component_name}' using query '{query_string}'."

        # Format retrieved chunks neatly with metadata section headers
        context_blocks = [
            f"Component Datasheet: {component_name}",
            "=============================================",
        ]

        for idx, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
            # Extract header path from LangChain's MarkdownHeaderTextSplitter metadata
            headers = [
                meta.get(f"Header {i}")
                for i in range(1, 4)
                if meta and meta.get(f"Header {i}")
            ]
            header_path = " > ".join(headers) if headers else "General Specifications"

            context_blocks.append(f"--- Chunk {idx} | Section: {header_path} ---")
            context_blocks.append(doc.strip())
            context_blocks.append("")  # Empty line separator

        return "\n".join(context_blocks)

    except Exception as e:
        logger.error("Error occurred while querying database: %s", e, exc_info=True)
        return f"Error retrieving context for component '{component_name}': {str(e)}"


if __name__ == "__main__":
    # Test query
    print("\n--- Running Test Live Retrieval Query ---")
    retrieved_spec = retrieve_context("MPU6050", "PWR_MGMT_1")
    print(retrieved_spec)
