from flask import Flask
from celery import Celery

app = Flask(__name__)
simple_app = Celery('tasks', broker='amqp://rabbitmq:5672')


@app.route('/simple_start_task')
def call_method():
    app.logger.info("Invoking Method ")
    r = simple_app.send_task('tasks.longtime_add', kwargs={'x': 1, 'y': 2})
    app.logger.info(r.backend)
    return r.id


@app.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/simple_task_result/<task_id>')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)


@app.route('/jobs', methods=["POST"])
def create_a_job():
    # get job name
    # get file
    # save file
    # save to db...
    # start the celery worker..

    # also need to create the empty outputfile in the output folder
    return "hi"


@app.route('/jobs', methods=["POST"])
def list_jobs():
    return "hi"


@app.route('/jobs/<job_id>', methods=["GET"])
def get_a_job():
    return "hi"


@app.route('/jobs/<job_id>', methods=["PATCH"])
def update_a_job():
    # update db
    return "hi"


@app.route('/jobs/<job_id>/results', methods=["GET"])
def download_a_job_results():
    # update db
    return "hi"


@app.route('/jobs/<job_id>/logs', methods=["GET"])
def download_a_job_logs():
    # update db
    return "hi"