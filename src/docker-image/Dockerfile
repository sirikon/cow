FROM debian:bookworm-slim AS docker-downloader
WORKDIR /builder
RUN apt-get update && apt-get install -y wget

# Download Docker
RUN echo "0a5f3157ce25532c5c1261a97acf3b25065cfe25940ef491fa01d5bea18ddc86  docker-24.0.5.tgz" > docker.sha256
RUN wget https://download.docker.com/linux/static/stable/x86_64/docker-24.0.5.tgz
RUN sha256sum -c docker.sha256
RUN tar -xvzf docker-24.0.5.tgz

# Download Docker Compose
RUN echo "f45e4cb687df8b48a57f656097ce7175fa8e8bef70be407b011e29ff663f475f  docker-compose-linux-x86_64" > docker-compose.sha256
RUN wget https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-linux-x86_64
RUN sha256sum -c docker-compose.sha256
RUN chmod +x docker-compose-linux-x86_64



FROM python:3.11-slim-bookworm as base
COPY ./src/cow/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY --from=docker-downloader /builder/docker/docker /usr/local/bin/docker
COPY --from=docker-downloader /builder/docker-compose-linux-x86_64 /usr/local/lib/docker/cli-plugins/docker-compose

FROM base AS vscode-dev-container

FROM base AS release
WORKDIR /app/src
COPY ./src/cow/src /app/src
CMD ["gunicorn", "--bind=0.0.0.0:80", "--workers=1", "cow.__main__:app"]
EXPOSE 80
