import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.database import db_helper

@pytest.mark.asyncio
async def test_db_connection():
    try:
        async with db_helper.session_getter() as session:
            result = await session.execute("SELECT 1")
            assert result.scalar() == 1
    except SQLAlchemyError as e:
        pytest.fail(f"Database connection failed: {e}")

@pytest.mark.asyncio
async def test_db_disconnection():
    try:
        await db_helper.dispose()
    except SQLAlchemyError as e:
        pytest.fail(f"Database disconnection failed: {e}")
