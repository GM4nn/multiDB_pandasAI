from sqlalchemy import Column, Float, Integer, String
from src.models.base import Base


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    ean = Column(String)
    name = Column(String)
    description = Column(String)
    img = Column(String)
    price = Column(String)
    price_with_discount = Column(String)
    department = Column(String)
    category = Column(String)
    subcategy = Column(String)