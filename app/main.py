from fastapi import FastAPI

from app.database import engine, Base
from app.models import Book
from app.routers.book import router as book_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Library Book Management API"
)


@app.get("/")
def home():
    return {
        "message": "Library API is running"
    }


app.include_router(book_router)