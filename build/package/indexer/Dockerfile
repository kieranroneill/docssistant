FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# setup pip version
COPY ./pip-requirements.txt .
RUN pip install --no-cache-dir -r pip-requirements.txt

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY ./.documents ./.documents
COPY ./pyproject.toml .
COPY ./indexer ./indexer
COPY ./libs ./libs

CMD ["python", "-m", "indexer.main"]
