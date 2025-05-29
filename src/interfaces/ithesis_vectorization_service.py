from abc import ABC, abstractmethod

class IThesisVectorizationService(ABC):

    @abstractmethod
    async def vectorize_theses(self):
        """
        Abstract method to vectorize theses from the database.
        """
        pass

    @abstractmethod
    async def get_vectorization_status(self) -> dict:
        pass


    # @abstractmethod
    # async def get_vectorized_theses(self):
    #     """
    #     Abstract method to retrieve vectorized theses from the database.
    #     """
    #     pass

    # @abstractmethod
    # async def delete_vectorized_theses(self):
    #     """
    #     Abstract method to delete vectorized theses from the database.
    #     """
    #     pass