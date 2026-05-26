import asyncio
import sys
from dotenv import load_dotenv

# Ensure environment variables are loaded before executing any server imports/actions
load_dotenv()

from MCP_Server import main

if __name__ == "__main__":
    print("SpecRAG Server (Server.py) booting up...", file=sys.stderr)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("SpecRAG Server shutting down gracefully.", file=sys.stderr)
