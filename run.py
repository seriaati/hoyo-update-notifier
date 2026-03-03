from __future__ import annotations
from pathlib import Path
from colorama import Fore, Style, init

import os

import uvicorn
from dotenv import load_dotenv

import hun

init(autoreset=True)

def info(msg: str):
    print(f"{Fore.GREEN}INFO:{Style.RESET_ALL} {msg}")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

if not DATA_DIR.exists():
    info(f"Creating data directory at {DATA_DIR}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(hun.app, port=int(os.getenv("PORT", "8092")), host=os.getenv("HOST", "127.0.0.1"))
