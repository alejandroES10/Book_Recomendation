# src/services/interfaces/thesis_data_importer_interface.py

from abc import ABC, abstractmethod

class IThesisDataImporterService(ABC):
    
    @abstractmethod
    async def upsert_theses(self):
        """
        Abstract method to upsert theses from an external source into the database.
        """
        pass
