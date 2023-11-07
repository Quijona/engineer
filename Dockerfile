FROM python:3.10

WORKDIR /app

# Copia el archivo requirements.txt al directorio /app
COPY requirements.txt .

# Instala las bibliotecas desde el archivo requirements.txt
RUN pip install -r requirements.txt

# Copia el script DEASAFIO_0.1.py al directorio /app
COPY DESAFIO_0.1.py .

# Ejecuta el script DEASAFIO_0.1.py
CMD ["python", "DESAFIO_0.1.py"]
