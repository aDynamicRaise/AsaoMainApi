from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped, mapped_column

from config import settings
from utils.case_converter import camel_case_to_snake_case

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)
    
    id: Mapped[int] = mapped_column(primary_key=True)

# на счет id, я его поставил как базовый, но он в целом может поменяться, 
# если у нас не int id будет, в таком случае можно добавить папку mixins, куда будем прописывать всякие виды id, и от них так же наследовать модели бд

class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=True)