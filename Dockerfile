# Multi-stage build to minimize final image size
FROM python:3.13.8-alpine AS builder

# Set build environment variables
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random

# Install build dependencies in one layer
RUN apk update && apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        cargo \
        rust \
        openssl \
    && rm -rf /var/cache/apk/*

# Create build user
RUN addgroup -g 1000 builduser && \
    adduser -u 1000 -G builduser -D -s /bin/bash builduser

USER builduser
WORKDIR /home/builduser

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --user --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --user "authlib>=1.6.4" && \
    pip install --no-cache-dir --user -r requirements.txt && \
    pip cache purge

# Final stage - minimal runtime image
FROM python:3.13.8-alpine AS runtime

# Set runtime environment variables
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PATH="/home/appuser/.local/bin:$PATH"

# Install only runtime dependencies
RUN apk update && apk add --no-cache \
        bash \
        shadow \
        su-exec \
        tini \
        grep \
        coreutils \
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/*

# Create application user
RUN addgroup -g 1000 appuser && \
    adduser -u 1000 -G appuser -D -s /bin/bash -h /home/appuser appuser

USER appuser
WORKDIR /home/appuser

# Copy Python packages from builder stage
COPY --from=builder --chown=appuser:appuser /home/builduser/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python3 -c "import sys; sys.exit(0)"

HEALTHCHECK --interval=60m --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f https://securenote.link/api/v1/health || exit 1

# Use tini as init system
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python3", "secure_note_mcp.py"]