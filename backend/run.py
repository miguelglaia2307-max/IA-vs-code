#!/usr/bin/env python
"""Entry point for running the backend server"""

import uvicorn
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    debug = os.getenv("DEBUG", "false").lower() == "true"
    workers = int(os.getenv("WORKERS", "1"))
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        workers=1 if debug else workers,
    )
