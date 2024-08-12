FROM tiangolo/uvicorn-gunicorn:python3.10

ENV MODULE_NAME=main
ENV MAX_WORKERS=1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY alembic.ini /app
# COPY ./alembic /app/alembic

COPY ./app /app/app

COPY main.py .
