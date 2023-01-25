FROM python:3.9

RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY "ingest_data.py" "ingest_data.py"

ENTRYPOINT [ "python", "ingest_data.py" ]