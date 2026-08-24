from fastapi import FastAPI, HTTPException
from backend.schemas import Transaction
from backend.predictor import predict
from backend.agent import investigate
from backend.llm import generate_explanation

app = FastAPI(title="AI Fraud Detection & Investigation Agent",version="1.0.0")

@app.get("/")
def root():
    return {"message":"AI Fraud Detection & Investigation Agent is running"}

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.post("/predict")
def prediction(transaction: Transaction):
    try:
        return predict(transaction.model_dump())
    except FileNotFoundError as e:
        raise HTTPException(500,str(e))

@app.post("/investigate")
def investigation(transaction: Transaction):
    try:
        data = transaction.model_dump()
        pred = predict(data)
        agent = investigate(data,pred)
        return {**pred,**agent,"explanation":generate_explanation(data,pred,agent)}
    except FileNotFoundError as e:
        raise HTTPException(500,str(e))
