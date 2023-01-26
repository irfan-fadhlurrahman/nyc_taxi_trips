FROM python:3.9

RUN pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY src src

ENTRYPOINT [ "python", "src/ingest_data.py" ]