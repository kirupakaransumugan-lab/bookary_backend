from fastapi import FastAPI

from app.database import engine, Base
from app.models import Book, Author, Category , Member , Borrow
from app.routers.book import router as book_router

from app.routers.author import router as author_router
from app.routers.category import router as category_router
from app.routers.members import router as member_router
from app.routers.borrow import router as borrow_router


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
app.include_router(author_router)
app.include_router(category_router)
app.include_router(member_router)
app.include_router(borrow_router)