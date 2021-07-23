from flask import Flask, request, Response, stream_with_context
from schemas import JobCreate
from service import create_item, list_items, get_item, download_logs, download_results, update_item

app = Flask(__name__)


# @app.route("/simple_start_task")
# def call_method():
#     app.logger.info("Invoking Method ")
#     r = simple_app.send_task("tasks.longtime_add", kwargs={"x": 1, "y": 2})
#     app.logger.info(r.backend)
#     return r.id


# @app.route("/simple_task_status/<task_id>")
# def get_status(task_id):
#     status = simple_app.AsyncResult(task_id, app=simple_app)
#     print("Invoking Method ")
#     return "Status of the Task " + str(status.state)


# @app.route("/simple_task_result/<task_id>")
# def task_result(task_id):
#     result = simple_app.AsyncResult(task_id).result
#     return "Result of the Task " + str(result)


@app.route("/jobs", methods=["POST"])
def create_a_job():
    app.logger.info("new upload is detected")
    file = request.files.get("file")
    name = request.form.get("name", None)

    item_create = JobCreate(name=name)
    try:
        item = create_item(file=file, item_create=item_create)
    except:
        pass
    return item.dict()


@app.route("/jobs", methods=["POST"])
def list_jobs():
    app.logger.info("list jobs...")
    items = list_items()
    return [x.dict() for x in items]


@app.route("/jobs/<job_id>", methods=["GET"])
def get_a_job(job_id):
    app.logger.info("list jobs...")
    item = get_item(job_id)
    return item.dict()


@app.route("/jobs/<job_id>", methods=["PATCH"])
def update_a_job(job_id):
    finished_rows = int(request.json['finished_rows'])
    item = update_item(finished_rows=finished_rows, item_id=job_id)
    return item.dict()


@app.route("/jobs/<job_id>/results", methods=["GET"])
def download_a_job_results(job_id):
    app.logger.info("download results")
    file = download_results(item_id=job_id)
    file_name = f"results_for_{job_id}.csv"
    return Response(
        stream_with_context(file),
        headers={
            "Content-Disposition": f'attachment;filename="{file_name}"',
        },
    )


@app.route("/jobs/<job_id>/logs", methods=["GET"])
def download_a_job_logs(job_id):
    app.logger.info("download logs")
    file = download_logs(item_id=job_id)
    file_name = f"logs_for_{job_id}.csv"
    return Response(
        stream_with_context(file),
        headers={
            "Content-Disposition": f'attachment;filename="{file_name}"',
        },
    )
