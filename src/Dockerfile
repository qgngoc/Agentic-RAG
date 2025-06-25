FROM python:3.12.11

RUN apt-get update && apt-get install python3-pip -y

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src

COPY . /src

# For production use, we use guvicorn as the ASGI server
# CMD ["guvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088", "--workers", "4"]

# For development use, we use uvicorn as the ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]