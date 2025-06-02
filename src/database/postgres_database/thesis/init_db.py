# init_db.py

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from ....models.thesis_model import Base

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)


DATABASE_CONFIG = {
    "DB_NAME": "dspace_db",
    "DB_USER": "postgres",
    "DB_PASSWORD": "postgres",
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
}

ASYNC_DB_URL = (
    f"postgresql+asyncpg://{DATABASE_CONFIG['DB_USER']}:{DATABASE_CONFIG['DB_PASSWORD']}"
    f"@{DATABASE_CONFIG['DB_HOST']}:{DATABASE_CONFIG['DB_PORT']}/{DATABASE_CONFIG['DB_NAME']}"
)

# Motor asíncrono con pool
engine = create_async_engine(
    ASYNC_DB_URL,
    echo=False,
    # pool_size=10,
    # max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)



def create_database_sync():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DATABASE_CONFIG['DB_USER'],
        password=DATABASE_CONFIG['DB_PASSWORD'],
        host=DATABASE_CONFIG['DB_HOST'],
        port=DATABASE_CONFIG['DB_PORT']
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DATABASE_CONFIG['DB_NAME'],))
    exists = cur.fetchone()

    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(DATABASE_CONFIG['DB_NAME'])))
        print(f"✅ Base de datos '{DATABASE_CONFIG['DB_NAME']}' creada.")
    else:
        print(f"ℹ️ La base de datos '{DATABASE_CONFIG['DB_NAME']}' ya existe.")

    cur.close()
    conn.close()


async def create_tables_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas/verificadas")


# main.py
import asyncio



async def main():
    await create_tables_async()


if __name__ == "__main__":
    asyncio.run(main())