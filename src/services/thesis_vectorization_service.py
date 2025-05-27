
import asyncio
from typing import List
from src.database.chromadb.thesis_collection import ThesisCollection
from src.database.postgres.thesis.thesis_repository import ThesisRepository
from src.database.postgres.thesis.init_db import AsyncSessionLocal

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


from src.interfaces.ithesis_vectorization_service import IThesisVectorizationService
from src.schemas.thesis_schema import ThesisSchema

class ThesisVectorizationService(IThesisVectorizationService):
    def __init__(self, thesis_collection: ThesisCollection, thesis_repository: ThesisRepository):
        self.thesis_collection = thesis_collection
        self.thesis_repository = thesis_repository

    async def vectorize_thesis(self):
        """
        Recorre las tesis no procesadas, filtra las que no están vectorizadas,
        las vectoriza y las marca como procesadas.
        """
        thesis_dtos = await self.extract_unprocessed_thesis_dtos()
        success_count = 0
        error_count = 0

        for dto in thesis_dtos:
            exists = await self.thesis_collection.exists_by_handle(dto.handle)
            if exists:
                async with AsyncSessionLocal() as session:
                    await self.thesis_repository.mark_as_processed(session, dto.handle)
                print(f"⏭️ Tesis ya vectorizada: {dto.handle}")
                continue

            try:
                enriched_fragments = await self.process_thesis_to_fragments(dto)
                await self.thesis_collection.add_documents(enriched_fragments)

                # ✅ Marcar como procesada en la base de datos
                async with AsyncSessionLocal() as session:
                    await self.thesis_repository.mark_as_processed(session, dto.handle)

                print(f"✅ Vectorizada y marcada como procesada: {dto.handle}")
                success_count += 1

            except Exception as e:
                print(f"❌ Error procesando {dto.handle}: {e}")
                error_count += 1

            print(f"\n📊 Resumen: {success_count} exitosas, {error_count} con error.")
        

    async def extract_unprocessed_thesis_dtos(self):
        """
        Gets all unprocessed theses and converts them into ThesisDto objects.
        """
        async with AsyncSessionLocal() as session:
            theses = await self.thesis_repository.get_non_vectorized_theses(session)

        return [
            ThesisSchema(
                handle=thesis.handle,
                metadata_json=thesis.metadata_json,
                original_name_document=thesis.original_name_document,
                size_bytes_document=thesis.size_bytes_document,
                download_url=thesis.download_url,
                is_processed=thesis.is_vectorized
            )
            for thesis in theses
        ]


        
    async def process_thesis_to_fragments(self, thesis_schema: ThesisSchema) -> List[Document]:
            """
            Procesa una tesis y devuelve sus fragmentos enriquecidos con metadatos.
            """
            loader = PyPDFLoader(thesis_schema.download_url)
            documents = await loader.aload()
            print("********Documento cargado********")
            print(documents)

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )
            splits = text_splitter.split_documents(documents)

            enriched_documents = []
            for fragment in splits:
                enriched_fragment = Document(
                    page_content=fragment.page_content,
                    metadata={
                        "handle": thesis_schema.handle,
                        "original_name_document": thesis_schema.original_name_document,
                        "size_bytes_document": thesis_schema.size_bytes_document,
                        **thesis_schema.metadata_json
                    }
                )
                print("********Fragmento com metadatos********")
                print(enriched_fragment)
                enriched_documents.append(enriched_fragment)

            return enriched_documents



#*********************************** Test **************************************
# async def main():
#     thesis_collection = ThesisCollection()  # Instancia según tu implementación real
#     thesis_repository = ThesisRepository()

#     vectorization_service = ThesisVectorizationService(thesis_collection, thesis_repository)
    
#     await vectorization_service.vectorize_thesis()

     

# if __name__ == "__main__":
#     asyncio.run(main())