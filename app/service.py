from contextlib import contextmanager
from app.db.database import SessionLocal
from schemas import Job, JobCreate
from repo import create, get, get_all
from typing import List
from fileManager import PersistentVolumnFileManager
from werkzeug.datastructures import FileStorage
import uuid
from celery import Celery

fm = PersistentVolumnFileManager()
simple_app = Celery('tasks', broker='amqp://rabbitmq:5672')

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


def create_item(
    file: FileStorage, item_create: JobCreate
) -> Job:
    """
    This function creates a file.
    """
    with get_db() as db:

        job_id = str(uuid.uuid4())
        size, rows = fm.upload_file(file=file, key=job_id)
        # create the version
        db_item = create(
            db=db,
            item=Job(
                id=job_id,
                name=item_create.name,
                size=size,
                rows=rows,
                finished_rows=0,
                done=False
            )
        )
        item = Job.from_orm(db_item)
    # time to start the celery task...
    r = simple_app.send_task('tasks.do_it', kwargs={'file_to_take': job_id, 'endpoint': 'simple_app:9001/random_number'})
    return item


def get_item(item_id: str) -> Job:
    with get_db() as db:
        db_item = get(db=db, item_id=item_id)
        item = Job.from_orm(db_item)
    return item

def list_items() -> List[Job]:
    with get_db() as db:
        db_items = get_all(db=db)
        items = [Job.from_orm(x) for x in db_items]
    return items
