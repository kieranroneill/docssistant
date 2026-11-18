FROM python:3.12-slim

WORKDIR /app

# setup pip version
COPY ./pip-requirements.txt .
RUN pip install --no-cache-dir -r pip-requirements.txt

# install dev dependencies
COPY ./dev-requirements.txt .
RUN pip install --no-cache-dir -r dev-requirements.txt

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY ./alembic.ini .
COPY ./api .
COPY ./migrations .

ENTRYPOINT ["alembic"]
