
from database.vector_store import vectorstore_of_books

class SearchService:
    def get_results(contentToSearch: str ):
        retriever = vectorstore_of_books.as_retriever(
             search_type="similarity",
            #  search_kwargs={"k": 2},
        ) 
        return retriever.batch([contentToSearch])
        



        