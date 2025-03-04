FROM python:3.12-slim

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/docker/server/entrypoint.sh
RUN chmod +x /app/docker/server/worker.sh