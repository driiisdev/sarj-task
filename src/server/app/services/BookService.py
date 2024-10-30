import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException
from aiocache import cached
from aiocache.serializers import JsonSerializer
from typing import Dict, Any, List
from sqlalchemy.exc import SQLAlchemyError
from app.models import Book
from app.schemas import BookSchema
from config.db import DBStorage

def extract_metadata(html_content: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {}

    meta_tags = {
        'title': 'og:title',
        'description': 'og:description',
        'type': 'og:type',
        'image': 'og:image',
        'url': 'og:url',
        'site_name': 'og:site_name'
    }

    for key, property_value in meta_tags.items():
        meta_tag = soup.find('meta', attrs={'property': property_value})
        if meta_tag:
            metadata[key] = meta_tag.get('content', '').strip()
        else:
            metadata[key] = None

    return metadata

def book_to_schema(book: Book) -> BookSchema:
    """Convert a Book model to BookSchema while ensuring all attributes are loaded."""
    return BookSchema(
        id=book.id,
        title=book.title,
        description=book.description,
        type=book.type,
        image=book.image,
        url=book.url,
        site_name=book.site_name,
        content=book.content
    )

@cached(ttl=3600, serializer=JsonSerializer())
async def get_book(book_id: str) -> BookSchema:
    try:
        # Check if book exists in database
        book = DBStorage.get(Book, book_id)
        if book:
            return book_to_schema(book)

        # If not, fetch from Project Gutenberg
        content_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        metadata_url = f"https://www.gutenberg.org/ebooks/{book_id}"

        async with aiohttp.ClientSession() as session:
            # Fetch content
            async with session.get(content_url) as content_response:
                if content_response.status != 200:
                    raise HTTPException(status_code=404, detail="No ebook by that number")
                content = await content_response.text()

            # Fetch metadata
            async with session.get(metadata_url) as metadata_response:
                if metadata_response.status == 200:
                    html_content = await metadata_response.text()
                    metadata = extract_metadata(html_content)
                else:
                    metadata = {}

        return BookSchema(id=book_id, content=content, **metadata)

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching book data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def save_book(book: BookSchema) -> BookSchema:
    try:
        new_book = Book(**book.dict())
        saved_book = DBStorage.new(new_book)
        return book_to_schema(saved_book)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error while saving book: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while saving book: {str(e)}")

async def get_saved_books() -> List[BookSchema]:
    try:
        books = DBStorage.all(Book)
        return [book_to_schema(book) for book in books]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error while retrieving books: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while retrieving books: {str(e)}")
    