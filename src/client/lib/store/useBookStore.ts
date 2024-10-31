import { create } from 'zustand';
import { Book } from '@/lib/types/book';

interface BookStore {
  bookId: string;
  selectedBook: Book | null;
  setBookId: (id: string) => void;
  setSelectedBook: (book: Book | null) => void;
}

export const useBookStore = create<BookStore>((set) => ({
  bookId: '',
  selectedBook: null,
  setBookId: (bookId) => set({ bookId }),
  setSelectedBook: (book) => set({ selectedBook: book }),
}));
