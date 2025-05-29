from typing import List

from fastapi import File


from abc import ABC, abstractmethod

class IGeneralInformationService(ABC):
    @abstractmethod
    async def add_general_info(self, file: File) -> dict:
        pass

    @abstractmethod
    async def get_general_info_by_vectorization_id(self, id: str) -> dict:
        pass

    @abstractmethod
    async def get_all_general_info(self) -> dict:
        pass

    @abstractmethod
    async def delete_general_info_by_vectorization_id(self, id: str) -> None:
        pass
