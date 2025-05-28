import asyncio
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.database.postgres.thesis.init_db import AsyncSessionLocal
from src.models.thesis_model import ProcessStatusModel, ProcessStatus, ProcessName

class ProcessStatusRepository:

    @staticmethod
    async def set_status(session: AsyncSession, process_name: str, status: ProcessStatus, error_messages: list = None):
        try:
            stmt = select(ProcessStatusModel).where(ProcessStatusModel.process_name == process_name)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            now = datetime.now()

            if existing:
                existing.status = status
                if status == ProcessStatus.RUNNING:
                    existing.started_at = now
                    existing.ended_at = None
                    existing.error_messages = None
                elif status in [ProcessStatus.COMPLETED, ProcessStatus.FAILED]:
                    existing.ended_at = now
                    existing.error_messages = error_messages or []
            else:
                new_status = ProcessStatusModel(
                    process_name= process_name,
                    status=status,
                    started_at=now if status == ProcessStatus.RUNNING else None,
                    ended_at=now if status in [ProcessStatus.COMPLETED, ProcessStatus.FAILED] else None,
                    error_messages=error_messages or []
                )
                session.add(new_status)

            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"[ERROR] No se pudo establecer el estado del proceso: {e}")

    @staticmethod
    async def get_status(session: AsyncSession, process_name: ProcessName) -> Optional[Dict[str, Any]]:
        try:
            stmt = select(ProcessStatusModel).where(ProcessStatusModel.process_name == process_name)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            if existing:
                return {
                    "process_name": existing.process_name.value,
                    "status": existing.status.value,  # como str
                    "started_at": existing.started_at.isoformat() if existing.started_at else None,
                    "ended_at": existing.ended_at.isoformat() if existing.ended_at else None,
                    "error_messages": existing.error_messages
                }
            return None
        except SQLAlchemyError as e:
            print(f"[ERROR] No se pudo obtener el estado del proceso: {e}")
            return None
        
    async def get_all_running_processes(session: AsyncSession):
        result = await session.execute(
            select(ProcessStatusModel).where(ProcessStatusModel.status == ProcessStatus.RUNNING)
        )
        return result.scalars().all()


# async def main():
#     async with AsyncSessionLocal() as session:
#         process = ProcessStatusRepository()
#         pn = ProcessName.IMPORT_THESIS
#         pe = ProcessStatus.RUNNING
#         await process.set_status(session,pn,pe)
#         print("Agregado el proceso")

#         info_process = await process.get_status(session,pn )
#         print("Proceso Existente")
#         print(info_process)



# if __name__ == "__main__":
#     asyncio.run(main())