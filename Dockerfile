FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app/app"

EXPOSE 8088

CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8088"]