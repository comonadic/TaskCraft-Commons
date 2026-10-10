FROM python:3.13-slim-bookworm
ENV PYTHONUNBUFFERED=1 MPLCONFIGDIR=/tmp/matplotlib OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
RUN apt-get update && apt-get install -y --no-install-recommends bash curl ca-certificates fonts-noto-cjk poppler-utils chromium libgl1 libegl1 libopengl0 ffmpeg libreoffice-calc && rm -rf /var/lib/apt/lists/*
COPY requirements-lock.txt /tmp/requirements-lock.txt
RUN pip install --no-cache-dir -r /tmp/requirements-lock.txt
COPY . /tests
RUN chmod 700 /tests
WORKDIR /app
