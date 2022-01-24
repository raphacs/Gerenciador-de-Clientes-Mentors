from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db_clientes_mentorstec.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class InsertDB(Base):
    __tablename__ = 'clientesMentors'
    id = Column(Integer, primary_key=True)
    id_cliente = Column(String)
    user_name = Column(String)
    pw_cliente = Column(String)