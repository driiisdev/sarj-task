'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { bookApi } from '@/actions/bookActions';
import { useBookStore } from '@/lib/store/useBookStore';
import { Book } from '@/lib/types/book';
import { ErrorMessage } from '@/components/ErrorMessage';
import { AnalysisSection } from './ui/components/BookAnalysis';

export default function Home() {
  const queryClient = useQueryClient();
  const { bookId, setSelectedBook, setBookId } = useBookStore();

  const { data: savedBooks, isLoading: isLoadingSaved, error: savedBooksError } = useQuery({
    queryKey: ['saved-books'],
    queryFn: bookApi.getSavedBooks,
  });

  const { data: searchedBook, isLoading: isSearching, error: searchError, refetch } = useQuery({
    queryKey: ['book', bookId],
    queryFn: () => bookApi.getBook(bookId),
    enabled: false,
    retry: false
  });

  const { mutate: saveBook, status, error: saveError } = useMutation({
    mutationFn: bookApi.saveBook,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-books'] });
    },
  });

  const handleSearch = () => {
    if (bookId) {
      refetch();
    }
  };

  const handleSave = (book: Book) => {
    saveBook(book);
    setSelectedBook(null);
  };

  return (
    <main className="h-screen flex flex-col">
      <section className="h-1/3 min-h-[250px] p-3 border-b">
        <div className="container mx-auto">
          <h1 className="text-lg font-base mb-1">Book Library</h1>
          <div className="flex flex-row justify-center space-x-2 mb-1">
            <input
              type="text"
              value={bookId}
              onChange={(e) => setBookId(e.target.value)}
              placeholder="Enter Book ID"
              className="px-2 py-1 outline-none border rounded text-black text-sm w-64"
            />
            <button
              onClick={handleSearch}
              disabled={isSearching}
              className="px-2 py-1 text-sm bg-blue-500 text-white rounded disabled:bg-gray-400"
            >
              {isSearching ? 'Searching...' : 'Search'}
            </button>
          </div>

          {searchError && <ErrorMessage message={searchError.message} />}

          {searchedBook && (
            <div className="flex justify-center items-start space-x-4 mt-5">
              <div className="h-32 w-24 flex-shrink-0">
                <img src={searchedBook.image} alt="" className="h-full w-full object-cover" />
              </div>
              <div className="flex flex-col space-y-1">
                <h6 className="font-semibold">{searchedBook.title}</h6>
                <p className="text-sm text-gray-600">Description: {searchedBook.description}</p>
                <p className="text-sm text-gray-600">Type: {searchedBook.type}</p>
                <p className="text-sm text-gray-600">ID: {searchedBook.id}</p>
                <button
                  onClick={() => handleSave(searchedBook)}
                  disabled={status === "pending"}
                  className="px-2 py-1 w-24 bg-green-500 text-white text-sm rounded disabled:bg-gray-400"
                >
                  {status === "pending" ? 'Saving...' : 'Save Book'}
                </button>
              </div>
            </div>
          )}
          {saveError && <ErrorMessage message={saveError.message} />}
        </div>
      </section>

      <section className="h-1/3 min-h-[250px] border-b overflow-y-auto">
        <div className="container mx-auto p-4">
          <AnalysisSection bookId={String(searchedBook?.id)} />
        </div>
      </section>

      <section className="h-1/3 min-h-[250px] overflow-y-auto">
        <div className="container mx-auto p-4">
          {isLoadingSaved ? (
            <p className="text-sm">Loading saved books...</p>
          ) : savedBooksError ? (
            <ErrorMessage message={savedBooksError.message} />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {savedBooks?.map((book) => (
                <div key={book.id} className="p-4 border rounded shadow-sm">
                  <div className="h-32 w-24 flex-shrink-0">
                    <img src={book.image} alt="" className="h-full w-full object-cover" />
                  </div>
                  <div className="flex flex-col space-y-1">
                    <h6 className="font-semibold">{book.title}</h6>
                    <p className="text-sm text-gray-600">Description: {book.description}</p>
                    <p className="text-sm text-gray-600">Type: {book.type}</p>
                    <p className="text-sm text-gray-600">ID: {book.id}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
