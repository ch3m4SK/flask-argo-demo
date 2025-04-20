FROM python:3.12-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app
COPY config.py run.py /app/

CMD ["python", "/app/run.py"]