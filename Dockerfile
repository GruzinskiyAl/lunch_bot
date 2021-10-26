FROM python:3.9.7-slim-buster

ENV PROJECT_ROOT=/src
WORKDIR $PROJECT_ROOT

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY . .

ENTRYPOINT ["python", "./app/main.py"]
