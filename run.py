from __future__ import annotations

import uvicorn

import hun

if __name__ == "__main__":
    uvicorn.run(hun.app, port=8092)
