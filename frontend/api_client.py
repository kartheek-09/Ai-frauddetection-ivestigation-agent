import os, requests
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("BACKEND_URL","http://127.0.0.1:8000")

def analyze_transaction(data):
    r = requests.post(f"{BASE_URL}/investigate",json=data,timeout=30)
    r.raise_for_status()
    return r.json()
