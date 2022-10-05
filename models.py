from enum import unique
from tkinter.tix import INTEGER
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True, nullable=False)

    stocks = relationship('Stock', back_populates='shop')

    def __str__(self):
        return f'Магазин {self.name}'


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=150), unique=True, nullable=False)

    books = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'{self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=150), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, back_populates='books')
    stocks = relationship('Stock', back_populates='book')


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, back_populates='stocks')
    shop = relationship(Shop, back_populates='stocks')
    sales = relationship('Sale', back_populates='stock')

    def __str__(self):
        return f'Склад {self.id}'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    stock = relationship(Stock, back_populates='sales')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)