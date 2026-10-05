import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database import (
    get_all_users,
    get_user_by_id,
    get_user_spending_analysis,
    get_user_transactions,
    get_all_credit_cards,
    get_card_by_id
)
from recommendation import get_recommendations_for_user

app = FastAPI(
    title="Credit-It AI API",
    description="Backend API for Credit-It AI-Powered Credit Card Recommendation System",
    version="1.0.0"
)

# Enable CORS for Flutter mobile client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount card images directory relative to project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE_DIR, "..", "flutter_app", "assets", "cards")
if os.path.exists(CARDS_DIR):
    app.mount("/static/cards", StaticFiles(directory=CARDS_DIR), name="card_images")

class ApplicationForm(BaseModel):
    user_id: str
    card_id: str
    pan: str
    dob: str
    full_name: str
    employment_type: str = "Salaried"
    monthly_income: float = 85000.0
    company_name: str = "Tech Corp Pvt Ltd"
    address: str = "Flat 402, Highrise Heights, Bandra West, Mumbai, Maharashtra"
    pincode: str = "400050"

@app.get("/")
def read_root():
    return {"message": "Welcome to Credit-It AI Recommendation API Service"}

@app.get("/api/users")
def list_users():
    return {"users": get_all_users()}

@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/{user_id}/spending")
def get_spending(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_user_spending_analysis(user_id)

@app.get("/api/users/{user_id}/transactions")
def get_transactions(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    txs = get_user_transactions(user_id)
    return {"user_id": user_id, "count": len(txs), "transactions": txs}

@app.get("/api/cards")
def list_cards():
    cards = get_all_credit_cards()
    return {"count": len(cards), "cards": cards}

@app.get("/api/cards/{card_id}")
def get_card(card_id: str):
    card = get_card_by_id(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.get("/api/recommendations/{user_id}")
def get_recommendations(user_id: str, category: str = Query("All")):
    rec = get_recommendations_for_user(user_id, category_filter=category)
    if not rec:
        raise HTTPException(status_code=404, detail="User not found or no recommendations available")
    return rec

@app.post("/api/applications")
def submit_application(form: ApplicationForm):
    card = get_card_by_id(form.card_id)
    user = get_user_by_id(form.user_id)
    if not card or not user:
        raise HTTPException(status_code=400, detail="Invalid card or user ID")
        
    application_id = f"APP_{form.user_id}_{form.card_id[:8].upper()}_9948"
    return {
        "status": "SUCCESS",
        "application_id": application_id,
        "message": f"Credit Card Application for {card['card_name']} submitted successfully!",
        "details": {
            "applicant_name": form.full_name,
            "pan": form.pan,
            "card_name": card["card_name"],
            "bank_name": card["bank_name"],
            "estimated_credit_limit": "₹2,50,000"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
