# Use an appropriate base image
FROM python:3.10

WORKDIR /app

COPY . /app/DESAFIO_0.1.py

CMD ["python", "DESAFIO_0.1.py"]







