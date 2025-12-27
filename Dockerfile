# Stage 1: builder for Python dependencies
FROM python:3.13.8-alpine AS builder

ENV \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random

# Install build tools
RUN apk update && apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        cargo \
        rust \
        openssl

# Create non-root build user
RUN addgroup -g 1000 builduser && \
    adduser -u 1000 -G builduser -D -s /bin/bash builduser

USER builduser
WORKDIR /home/builduser

# Copy only requirements
COPY requirements.txt .

# Install secure pinned Python deps
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install --user -r requirements.txt

# Final runtime stage
FROM python:3.13.8-alpine AS runtime

ENV \
    PATH="/home/appuser/.local/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

# Install only runtime packages
RUN apk update && apk add --no-cache \
        bash \
        tini \
        grep \
        coreutils \
    && rm -rf /var/cache/apk/*

# Create non-root app user
RUN addgroup -g 1000 appuser && \
    adduser -u 1000 -G appuser -D -s /bin/bash -h /home/appuser appuser

USER appuser
WORKDIR /home/appuser

# Copy installed packages from builder
COPY --from=builder --chown=appuser:appuser /home/builduser/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Healthcheck
HEALTHCHECK --interval=60m --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f https://securenote.link/api/v1/health || exit 1

# Entrypoint with tini for signal handling
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python3", "secure_note_mcp.py"]
