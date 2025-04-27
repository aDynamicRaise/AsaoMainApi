from datetime import timezone, datetime
from typing import Optional
from sqlalchemy import CHAR, Float, ForeignKey, MetaData, Text, text
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped, mapped_column

from auth.schemas import UserPassSchema, UserRead
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
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)

    def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id,
            name=self.name,
            email=self.email
        )

class UserPasses(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    hash_pass: Mapped[str] = mapped_column()
    date_pass: Mapped[datetime] = mapped_column(default=datetime.now())

    def to_read_model(self) -> UserPassSchema:
        return UserPassSchema(
            user_id=self.user_id,
            hash_pass=self.hash_pass,
            date_pass=self.date_pass
        )


class Product(Base):
    __tablename__ = "product"

    name: Mapped[str]
    link: Mapped[str]
    seller_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)

    data_history: Mapped[list["ProductData"]] = relationship("ProductData", back_populates="product")


class ProductData(Base):
    __tablename__ = "product_data"

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    date_receipt: Mapped[datetime]
    # ozon_card_price: Mapped[float | None]
    # discount_price: Mapped[float | None]
    ozon_card_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True) 
    discount_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True) 
    base_price: Mapped[float]
    star_count: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    review_count: Mapped[Optional[int]] = mapped_column(nullable=True)



    product: Mapped["Product"] = relationship("Product", back_populates="data_history")

