from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.auth.router import router as auth_router
from app.facebook.router import router as facebook_router
from app.routes.pages import router as pages_router

app = FastAPI(
    title="Facebook Marketing API Integration",
    description="Server-side OAuth and Insights ingestion for Facebook Marketing API",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()


# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(facebook_router, prefix="/facebook", tags=["Facebook Marketing API"])
app.include_router(pages_router, tags=["Pages"])


@app.get("/")
def root():
    return {"message": "Facebook Marketing API Integration - FastAPI", "status": "running"}