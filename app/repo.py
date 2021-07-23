from sqlalchemy.sql.expression import and_, or_
from schemas import Job as JobSchema
from app.db.models import Job as JobModel
from sqlalchemy.orm import Session


def create(db: Session, item: JobSchema) -> JobModel:
    db_item = JobModel(
        id=item.id,
        name=item.name,
        size=item.size,
        rows=item.rows,
        finished_rows=item.finished_rows,
        done=item.done,
    )
    db.add(db_item)
    return db_item


def get(db: Session, item_id: str) -> JobModel:
    return db.query(JobModel).filter(JobModel.id == item_id).first()


def get_all(db: Session):
    return db.query(JobModel).all()
