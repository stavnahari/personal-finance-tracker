from fastapi import FastAPI
from backend.routers import auth, transactions, analytics
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Personal Finance Tracker")

# Allow frontend during development
origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # CRA
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

@app.get("/")
def root():
    return {"message": "Finance Tracker API is running 🚀"} 