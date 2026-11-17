import sys
import os
from pathlib import Path

# Add backend directory to sys.path so backend imports (like src.database, src.routers, etc.) resolve properly
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import the FastAPI application instance
from main import app
