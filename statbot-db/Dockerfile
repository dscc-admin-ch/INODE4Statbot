# Stage 1: Build MinIO client from source using Go
FROM golang:1.24-alpine AS builder
RUN go install github.com/minio/mc@latest

# Stage 2: Final PostgreSQL image
FROM postgres:16-bookworm

USER root

# Install tools needed to extract the backup
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        tar \
    && rm -rf /var/lib/apt/lists/*

# Copy the compiled 'mc' binary from the builder stage
COPY --from=builder /go/bin/mc /usr/local/bin/mc
RUN chmod +x /usr/local/bin/mc

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]