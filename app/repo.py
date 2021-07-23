from sqlalchemy.sql.expression import and_, or_
from schemas import Job as JobSchema
from db.models import Job as JobModel
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
    return (
        db.query(JobModel)
        .filter(JobModel.id == item_id)
        .order_by(JobModel.name.desc())
        .first()
    )


def get_all(db: Session):
    return db.query(JobModel).all()


def update(db: Session, item_id: str, finished_rows: int) -> JobModel:
    item = get(db=db, item_id=item_id)
    item.finished_rows = finished_rows
    return item
