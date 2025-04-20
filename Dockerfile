FROM python:3.12-slim

WORKDIR /app

# Copia TODOS los archivos necesarios
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r app/requirements.txt

# Establece PYTHONPATH para que Python encuentre los módulos
ENV PYTHONPATH=/app

CMD ["python", "run.py"]