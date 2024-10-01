FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "your_app.py"]
