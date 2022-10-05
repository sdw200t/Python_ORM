import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Shop, Publisher, Book, Stock, Sale 
from uploadData import uploadDataToDb 

DSN = 'postgresql://postgres:postgres@localhost:5432/bookstore'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

# Создание таблиц базы данных
create_tables(engine)

# Наполнение базы данных данными
uploadDataToDb(session)

# Выводим список издателей
for c in session.query(Publisher).all():
    print(c)

#Выводит издателя (publisher), имя или идентификатор которого принимается через input().
while True:
    publisher = input('Введите номер издателя (для выхода введите 0): ')
    if publisher == '0':
        break

    subquery = session.query(Stock).join(Book.stocks).filter(Book.id_publisher==publisher).subquery()
    for c in session.query(Shop).join(subquery, Shop.id == subquery.c.id_shop).all():
        print(c)

session.close()