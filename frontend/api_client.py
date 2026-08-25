import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BACKEND_URL","http://127.0.0.1:8000")

def analyze_transaction(data):
    try:
        response = requests.post(
            f"{BASE_URL}/investigate",
            json=data,
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Could not connect to the backend at {BASE_URL}. "
            "Make sure the FastAPI server is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The backend request timed out. Please try again."
        )

    except requests.exceptions.HTTPError as e:
        try:
            detail = response.json()
        except Exception:
            detail = response.text

        raise RuntimeError(
            f"Backend returned an error: {detail}"
        ) from e

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Request to backend failed: {e}"
        ) from e