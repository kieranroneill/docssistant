FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

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
COPY ./pyproject.toml .
COPY ./api .
COPY ./migrations .

CMD ["python", "-m", "api.main"]
