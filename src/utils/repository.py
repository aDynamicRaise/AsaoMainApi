
from sqlalchemy.exc import SQLAlchemyError

from abc import ABC, abstractmethod

from sqlalchemy import insert, select

from database.connection import get_async_session
from database.db_helper import db_helper



class AbstractRepository(ABC):
    @abstractmethod
    def add_one():
        raise NotImplementedError

    @abstractmethod
    def get_all():
        raise NotImplementedError



class SQLAlchemyRepository(AbstractRepository):
    model = None


    @classmethod
    async def add_one(self, data: dict):
        async with db_helper.session_getter() as session:
            item = self.model(**data)
            try:
                session.add(item)
                await session.commit()
                return item
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            

    @classmethod
    async def get_all(self):
        async with db_helper.session_getter() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            result = [row[0].to_read_model() for row in result.all()]
            return result

    
    @classmethod
    async def get_by_id(self, id):
        async with db_helper.session_getter() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            if not result:
                return None
            return result.scalars().first().to_read_model()
        
    
        
