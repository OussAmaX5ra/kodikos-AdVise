from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

router = APIRouter()


# ============ Request/Response Models ============
class AskAIRequest(BaseModel):
    question: str


class AskAIResponse(BaseModel):
    answer: str


# ============ Public Pages ============
@router.get("/public/landing")
def landing_page():
    """Landing page placeholder."""
    return {
        "page": "landing",
        "message": "Welcome to AdsAi"
    }


@router.get("/public/login")
def login_page():
    """Login page placeholder."""
    return {
        "page": "login"
    }


@router.get("/public/signup")
def signup_page():
    """Signup page placeholder."""
    return {
        "page": "signup"
    }


# ============ Dashboard ============
@router.get("/dashboard")
def dashboard_page():
    """Dashboard placeholder."""
    return {
        "page": "dashboard",
        "summary": "Placeholder dashboard data"
    }


# ============ Reports & Analytics ============
@router.get("/reports")
def reports_page():
    """Reports and analytics placeholder."""
    return {
        "page": "reports",
        "charts": []
    }


@router.post("/reports/upload")
async def upload_report(file: UploadFile = File(...)):
    """Upload CSV file placeholder. Does not process the file."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    return {
        "filename": file.filename,
        "message": "File uploaded successfully (not processed)"
    }


# ============ Manage Accounts ============
@router.get("/accounts/manage")
def manage_accounts_page():
    """Manage accounts placeholder."""
    return {
        "page": "manage_accounts",
        "accounts": []
    }


# ============ AI Assistant ============
@router.get("/ai")
def ai_assistant_page():
    """AI assistant placeholder."""
    return {
        "page": "ai_assistant",
        "status": "ready"
    }


@router.post("/ai/ask", response_model=AskAIResponse)
def ask_ai(request: AskAIRequest):
    """AI assistant question endpoint placeholder."""
    return {
        "answer": f"Placeholder response to: {request.question}"
    }


# ============ Campaigns ============
@router.get("/campaigns")
def campaigns_page():
    """Campaigns page placeholder."""
    return {
        "page": "campaigns",
        "campaigns": []
    }