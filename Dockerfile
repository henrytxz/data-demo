FROM python:3.9-slim-bullseye

COPY requirements.txt ./

RUN pip install -U pip && \
    pip install -r requirements.txt \
    --no-cache-dir

ENV DBT_DIR /dbt
ENV DBT_PROFILES_DIR $DBT_DIR

WORKDIR $DBT_DIR

COPY dbt ./

RUN dbt deps
