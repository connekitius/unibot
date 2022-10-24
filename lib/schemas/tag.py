from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tag(Base):
	__tablename__ = 'tags'
	id = Column(String(7), primary_key=True, unique=True)
	author_id = Column(Integer, nullable=False)
	title = Column(String(50), nullable=True)
	description = Column(String(500), nullable=False)
	created_at = Column(DateTime(), nullable=True)