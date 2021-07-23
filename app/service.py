from contextlib import contextmanager
from db.database import SessionLocal
from schemas import Job, JobCreate, JobUpdate
from repo import create, get, get_all, update
from typing import List, Tuple
from fileManager import PersistentVolumnFileManager
from werkzeug.datastructures import FileStorage
import uuid
from celery import Celery
import logging


fm = PersistentVolumnFileManager()
celery_app = Celery("tasks", broker="amqp://rabbitmq:5672")
logger = logging.getLogger(__name__)


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


def create_item(file: FileStorage, item_create: JobCreate) -> Job:
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
                done=False,
            ),
        )
        item = Job.from_orm(db_item)
    # time to start the celery task...
    r = celery_app.send_task(
        "tasks.do_it",
        kwargs={"job_id": job_id, "endpoint": "simple_app:9001/random_number"},
    )
    logger.info(r.backend)
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


def update_item(finished_rows: int, item_id: str) -> Job:
    with get_db() as db:
        db_item = update(db=db, item_id=item_id, finished_rows=finished_rows)
        item = Job.from_orm(db_item)
    return item


def download_results(
    item_id: str
) -> bytes:
    file = fm.download_file(key=item_id, logs=False)
    return file


def download_logs(
    item_id: str
) -> bytes:
    file = fm.download_file(key=item_id, logs=True)
    return file


# def download_item(
#     dataset_id: str, file_id: str, version: int = None
# ) -> Tuple[bytes, str, int]:
#     with session_scope() as db:
#         db_file = fileRepo.get(db=db, dataset_id=dataset_id, file_id=file_id)
#         file_name = db_file.name
#         storage_type = db_file.storage_type

#         if version is None:
#             db_file_version = fileVersionRepo.get_latest(db=db, file_id=file_id)
#         else:
#             db_file_version = fileVersionRepo.get_by_version(
#                 db=db, file_id=file_id, version=version
#             )
#         key = db_file_version.id
#         size = db_file_version.size
#     fm = get_file_manager(storage_type=storage_type)
#     file = fm.download_file(key=key)
#     return file, file_name, size