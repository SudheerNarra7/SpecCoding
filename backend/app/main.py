from fastapi import FastAPI
from .api.v1 import auth, users
from .core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

@app.get("/health")
def health_check():
    return {"status": "ok"}