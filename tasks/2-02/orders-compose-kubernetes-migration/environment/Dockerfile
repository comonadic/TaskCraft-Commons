FROM python:3.13-slim-bookworm
ENV PYTHONUNBUFFERED=1 MPLCONFIGDIR=/tmp/matplotlib OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
RUN apt-get update && apt-get install -y --no-install-recommends bash curl ca-certificates fonts-noto-cjk poppler-utils chromium libgl1 libegl1 libopengl0 ffmpeg libreoffice-calc && rm -rf /var/lib/apt/lists/*
COPY requirements-lock.txt /tmp/requirements-lock.txt
RUN pip install --no-cache-dir -r /tmp/requirements-lock.txt
RUN apt-get update && apt-get install -y --no-install-recommends iproute2 iptables conntrack kmod socat util-linux && rm -rf /var/lib/apt/lists/*
COPY assets/k3s /usr/local/bin/k3s
COPY assets/helm-linux-arm64.tar.gz /tmp/helm.tar.gz
RUN tar -xzf /tmp/helm.tar.gz -C /tmp && mv /tmp/linux-arm64/helm /usr/local/bin/helm && chmod +x /usr/local/bin/k3s && ln -s /usr/local/bin/k3s /usr/local/bin/kubectl
COPY assets/k3s-airgap-images-arm64.tar.zst assets/python.tar assets/postgres.tar assets/webapp.tar /var/lib/rancher/k3s/agent/images/
COPY input /app/input
COPY software /app/software
RUN mkdir -p /app/output && chmod -R a-w /app/input && chmod +x /app/software/*.sh
ENV KUBECONFIG=/etc/rancher/k3s/k3s.yaml
WORKDIR /app
CMD ["sleep","infinity"]
