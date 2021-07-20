FROM python:3.9

WORKDIR /opt/yijunx/code

COPY './requirements.txt' .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT celery -A tasks worker --loglevel=info
