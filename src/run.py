import sys
import os
import uvicorn

from src.setup.config import config

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # optional
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # ensures root is included


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=config.port, reload=True)
