import baseUrl  from "@/lib/config/config";
import { Book, SuccessResponse } from '@/lib/types/book';
import { ApiError } from '@/lib/types/error';

async function handleApiError(response: Response) {
  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail);
  }
}


class BookApi {
  
  getBook = async (id: string): Promise<Book> => {
    try {
      const response = await fetch(`${baseUrl}/book/${id}`);
      await handleApiError(response);
      return await response.json();
    } catch (error) {
      throw new Error(`Failed to fetch book: ${error}`);
    }
  }

  saveBook = async (book: Book): Promise<SuccessResponse> =>{
    try {
      const response = await fetch(`${baseUrl}/book`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(book),
      });
      await handleApiError(response);
      return await response.json();
    } catch (error) {
      throw new Error(`Failed to save book: ${error}`);
    }
  }

  getSavedBooks = async (): Promise<Book[]> => {
    try {
      const response = await fetch(`${baseUrl}/books`);
      await handleApiError(response);
      return await response.json();
    } catch (error) {
      throw new Error(`Failed to fetch saved books: ${error}`);
    }
  }
} 

export const bookApi = new BookApi();
