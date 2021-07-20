from contextlib import contextmanager
from app.db.database import SessionLocal
from schemas import Job as JobSchema
from repo import create, get, get_all
from typing import List


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def create_item(item: JobSchema) -> JobSchema:
    with get_db() as db:
        db_item = create(db=db, item=item)
        item = JobSchema.from_orm(db_item)
    return item


def get_item(item_id: str) -> JobSchema:
    with get_db() as db:
        db_item = get(db=db, item_id=item_id)
        item = JobSchema.from_orm(db_item)
    return item

def list_items() -> List[JobSchema]:
    with get_db() as db:
        db_items = get_all(db=db)
        items = [JobSchema.from_orm(x) for x in db_items]
    return items
