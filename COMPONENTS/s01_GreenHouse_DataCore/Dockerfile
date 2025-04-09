FROM python:3-alpine AS builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["hypercorn", "main:app", "--bind", "::"]