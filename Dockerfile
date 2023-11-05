# Use an appropriate base image
FROM python:3.10

# Set the working directory within the image
WORKDIR /app

# Copy the local file to the working directory in the image
COPY . /app/DESAFIO_0.1.py


# Rest of your Dockerfile

#RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run when the container is started
CMD ["python", "DESAFIO_0.1.py"]







