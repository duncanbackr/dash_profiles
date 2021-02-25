ARG ENV

# Builder with dev dependencies
FROM python:3.8-slim-buster AS dev_builder
COPY Pipfile* /tmp/
RUN \
    pip install --upgrade pip && \
    cd /tmp && \
    pip install pipenv && \
    pipenv lock --requirements -d > requirements.txt

# Builder without dev dependencies
FROM python:3.8-slim-buster AS builder
COPY Pipfile* /tmp/
RUN \
    pip install --upgrade pip && \
    cd /tmp && \
    pip install pipenv && \
    pipenv lock --requirements > requirements.txt

# Local version
FROM python:3.8-slim-buster as dev
ENV APP_HOME=/template
WORKDIR $APP_HOME
COPY --from=dev_builder /tmp/requirements.txt /tmp/requirements.txt
CMD python manage.py run -h 0.0.0.0$PORT

# Staging version
FROM python:3.8-slim-buster as backr-dev
ENV APP_HOME=/template
WORKDIR $APP_HOME
COPY --from=builder /tmp/requirements.txt /tmp/requirements.txt
COPY . .
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 "app:create_app()"

# Prod version
FROM python:3.8-slim-buster as backr-prod
ENV APP_HOME=/template
WORKDIR $APP_HOME
COPY --from=builder /tmp/requirements.txt /tmp/requirements.txt
COPY . .
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 "manage:create_app()"

# Final version
FROM ${ENV} AS final
RUN \
    apt-get update && \
    apt-get upgrade -y && \
    cd /tmp && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean
