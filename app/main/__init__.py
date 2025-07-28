from fastapi import FastAPI
from app.routers import account


app = FastAPI()

app.include_router(account.router)