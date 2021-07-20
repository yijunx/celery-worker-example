import time
from celery import Celery
from celery.utils.log import get_task_logger
import requests
import os

logger = get_task_logger(__name__)
app = Celery("tasks", broker="amqp://rabbitmq:5672")
INPUT_DATA_STORAGE_FOLDER = "/opt/yijunx/data_inputs"
OUTPUT_DATA_STORAGE_FOLDER = "/opt/yijunx/data_outputs"
APP_BASE_URL = "batchjobapp:9000"  # comes from envvar


@app.task()
def do_it(job_id: str, endpoint: str):

    # from the job id, it fetches the input file
    # reading the input file then it start to work...

    # open the file and loop it...suppose its a csv... to be easy
    row = 0
    with open(os.path.join(INPUT_DATA_STORAGE_FOLDER, job_id), "r") as f_in:
        with open(os.path.join(OUTPUT_DATA_STORAGE_FOLDER, job_id), "a") as f_out:

            for l in f_in:
                try:
                    r = requests.post(url=endpoint, json={"something": l})
                    # check the status of r and do log here!!!!

                    # save the result in the output folder with a method to append
                    # csv of payload and data
                    f_out.write(f"{l},{r.json()['random_number']}" + "\n")
                except:
                    # do log here!!!!
                    pass
                finally:
                    row += 1
                    if row % 5 == 0:
                        requests.patch(
                            url=f"{APP_BASE_URL}/jobs/{job_id}",
                            json={"finished_rows": row},
                        )
    requests.patch(url=f"{APP_BASE_URL}/jobs/{job_id}", json={"finished_rows": row})

