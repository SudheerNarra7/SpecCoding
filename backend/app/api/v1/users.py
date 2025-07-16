from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_user_routes():
    return {"message": "user routes"}
