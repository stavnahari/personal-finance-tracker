from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    # placeholder until JWT logic
    return {"msg": f"User {username} logged in"}
