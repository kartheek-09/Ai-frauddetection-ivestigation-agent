import os
from dotenv import load_dotenv
load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH","models/fraud_model.joblib")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","")
