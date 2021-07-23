# just an example for flask + celery to do tasks #

### intro ###

This repo has 3 parts:
    - 
        app is the main driver, it tells celery_app to work on a job, and celery_app will report the progress back to app. The job starts with a csv file or any file which can be read line by line. app stores the metadata of the job in postgres, and send the job_id to celery_worker.
    - 
        celery_app is the worker, it receives job from app, and do the job. The actual job is sending each line of the csv provided by app to simple_app, in order to get a response, then store the response in csv. celery_app can find the input csv because of the job_id provided by app, and because app and celery_app mounts to same volumn
    - 
        simple_app is an api service to process a line in the csv file, and provide a response.

### how to set up ###

    docker network create micro-services
    cd app
    make up

### how to use it ###

Please check app.py in app to see the endpoints..
