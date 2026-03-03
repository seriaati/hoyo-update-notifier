from __future__ import annotations

import os

import uvicorn
from dotenv import load_dotenv

import hun

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(hun.app, port=int(os.getenv("PORT", "8092")), host=os.getenv("HOST", "127.0.0.1"))
