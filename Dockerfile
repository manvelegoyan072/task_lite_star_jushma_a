FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY . .

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]