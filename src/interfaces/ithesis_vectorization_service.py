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


    