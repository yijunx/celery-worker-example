import time
from celery import Celery
from celery.utils.log import get_task_logger
import requests

logger = get_task_logger(__name__)
app = Celery('tasks', broker='amqp://rabbitmq:5672')
output_folder = ""
app_base_url = "batchjobapp:9000"  # comes from envvar

@app.task()
def do_a_job(job_id: str, row: int, total_row: int, payload: dict, do_job_endpoint: str):
    try:
        r = requests.post(url=do_job_endpoint, json=payload)
        # check the status of r and do log here!!!!

        # save the result in the output folder with a method to append
        # csv of payload and data
    except:
        # do log here!!!!
        pass
    finally:
        pass
    # reporting! for status...
    # write to log how is the progress

    # report the status
    if row % 5 == 0 or row == total_row:
        requests.patch(url=f"{app_base_url}/jobs/{job_id}", json={
            "finished_rows": row
        })


    # return x + y

# celery -A tasks worker --loglevel=info