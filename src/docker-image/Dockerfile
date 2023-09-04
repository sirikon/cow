FROM debian:bookworm-slim AS builder
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

FROM python:3.11-slim-bookworm as release
WORKDIR /app
COPY ./src/cow/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/cow/src ./src
WORKDIR /app/src
CMD ["flask", "--app", "cow.__main__", "run", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80

COPY --from=builder /builder/docker/docker /usr/local/bin/docker
COPY --from=builder /builder/docker-compose-linux-x86_64 /usr/local/lib/docker/cli-plugins/docker-compose

FROM release AS development
CMD ["flask", "--app", "cow.__main__", "run", "--host", "0.0.0.0", "--port", "80", "--debug"]