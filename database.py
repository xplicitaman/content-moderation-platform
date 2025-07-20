# handles the connection logic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://moderation_user:moderation_pass@localhost:5432/moderation_db"  # Connection String

engine = create_async_engine(DATABASE_URL, echo=True)   # Main connection interface to the database
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)   # "session factory" that creates individual database sessions for each request