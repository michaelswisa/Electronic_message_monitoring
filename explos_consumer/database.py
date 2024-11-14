from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

connection_url = 'postgresql://michael:1234@db-sql:5432/explos_db'
engine = create_engine(connection_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)

