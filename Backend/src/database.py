
from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine

class Card(SQLModel, table=True):
    id: Optional[UUID] = Field(primary_key=True, default=None)
    front: str = Field(default=None)
    front_inside: str = Field(default=None)
    back_inside: str = Field(default=None)
    back: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]