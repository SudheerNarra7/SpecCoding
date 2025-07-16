from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_auth_routes():
    return {"message": "auth routes"}