FROM python:3.12.11

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY requirements.txt requirements.txt

RUN uv pip install --system --no-cache-dir -r requirements.txt

WORKDIR /src

COPY . /src

# For production use, we use guvicorn as the ASGI server
# CMD ["guvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088", "--workers", "4"]

# For development use, we use uvicorn as the ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]