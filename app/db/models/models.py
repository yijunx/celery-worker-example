from sqlalchemy import Column, String, DateTime, UniqueConstraint, BigInteger, Integer
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from .base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    size = Column(BigInteger, nullable=False)
    rows = Column(Integer, nullable=False)
    finished_rows = Column(Integer, nullable=False)
    done = Column(Boolean, nullable=False)
