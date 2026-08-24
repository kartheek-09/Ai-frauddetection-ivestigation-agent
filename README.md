# AI Fraud Detection & Investigation Agent

Small AIML project: ML model + investigation agent + FastAPI + Streamlit + Render.

## Run
```powershell
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
python training/generate_data.py
python training/train.py
uvicorn backend.main:app --reload
```
In another terminal:
```powershell
streamlit run frontend/app.py
```

Optional Gemini: copy `.env.example` to `.env` and add `GEMINI_API_KEY`. The app works without it using a rule-based explanation fallback.

Render start command:
`uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

The dataset is synthetic and intended for learning/demo purposes.
