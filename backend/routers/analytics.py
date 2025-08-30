from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def analytics_summary():
    return {"spending": 1500, "income": 2500}
