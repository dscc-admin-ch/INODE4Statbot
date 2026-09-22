FROM postgres:16-bookworm

USER root

# Install tools needed to download/extract the backup
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       ca-certificates \
       tar \
    && rm -rf /var/lib/apt/lists/*

# Install MinIO client
RUN curl -fsSL https://dl.min.io/client/mc/release/linux-amd64/mc \
    -o /usr/local/bin/mc \
    && chmod +x /usr/local/bin/mc

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
