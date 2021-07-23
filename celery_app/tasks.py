import time
from celery import Celery
from celery.utils.log import get_task_logger
import requests
import os

logger = get_task_logger(__name__)
app = Celery("tasks", broker="amqp://rabbitmq:5672")
INPUT_DATA_STORAGE_FOLDER = "/opt/yijunx/data_inputs"
OUTPUT_DATA_STORAGE_FOLDER = "/opt/yijunx/data_outputs"
LOG_STORAGE_FOLDER = "/opt/yijunx/task_logs"
APP_BASE_URL = "http://batchjobapp:8000"  # comes from envvar


@app.task()
def do_it(job_id: str, endpoint: str):

    # from the job id, it fetches the input file
    # reading the input file then it start to work...

    # open the file and loop it...suppose its a csv... to be easy
    row = 0
    with open(os.path.join(INPUT_DATA_STORAGE_FOLDER, job_id), "r") as f_in:
        with open(os.path.join(OUTPUT_DATA_STORAGE_FOLDER, job_id), "a") as f_out:
            with open(os.path.join(LOG_STORAGE_FOLDER, job_id), "a") as f_log:
                for l in f_in:
                    try:
                        f_log.write(f"{endpoint},{l}")
                        r = requests.post(url=endpoint, json={"something": l})
                        if r.status_code == 200:
                            f_out.write(f"{l},{r.json()['random_number']}" + "\n")
                        else:
                            f_out.write(f"{l}," + "\n")
                    except:
                        f_log.write(f"cannot get even status code.." + "\n")
                    finally:
                        row += 1
                        if row % 5 == 0:
                            requests.patch(
                                url=f"{APP_BASE_URL}/jobs/{job_id}",
                                json={"finished_rows": row},
                            )
    requests.patch(url=f"{APP_BASE_URL}/jobs/{job_id}", json={"finished_rows": row})

