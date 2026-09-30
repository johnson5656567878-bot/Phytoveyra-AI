import sys
import os

# Add apps/api to path so FastAPI imports and models resolve cleanly
api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "api"))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from app.main import app
