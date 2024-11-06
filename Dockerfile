FROM python:3.12.7-slim@sha256:032c52613401895aa3d418a4c563d2d05f993bc3ecc065c8f4e2280978acd249 AS base
ARG TARGETPLATFORM
WORKDIR /app

# hadolint ignore=DL3008
RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get -y install --no-install-recommends \
    build-essential; \
    apt-get clean; rm -rf /var/lib/apt/lists/*; \
fi

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip check

RUN pip install memray

FROM base AS production
COPY main.py .
COPY app.py .
ENTRYPOINT ["memray", "run", "/app/main.py"]
