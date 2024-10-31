from fastapi import APIRouter

from app.controllers import BookController
from app.schemas import BookSchema, SuccessResponse

router = APIRouter()

@router.get("/book/{book_id}", response_model=BookSchema)
async def get_book(book_id: str):
    return await BookController.get_book(book_id)

@router.post("/book", response_model=SuccessResponse)
async def save_book(book: BookSchema):
    return await BookController.save_book(book)

@router.get("/books", response_model=list[BookSchema])
async def get_saved_books():
    return await BookController.get_saved_books()
