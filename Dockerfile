# Use a glibc-based Python 3.14 image (beta)
FROM python:3.11-slim


# Set environment variables
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /

# Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     curl \
#     gcc \
#     git \
#     libffi-dev \
#     libssl-dev \
#     pkg-config \
#     rustc \
#     cargo \
#     bash \
#     && rm -rf /var/lib/apt/lists/*

# Optional: upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Copy code into container
COPY . .

# Make setup script executable and run it
RUN chmod +x setup_mcp.sh && ./setup_mcp.sh

# (Optional) Expose ports if needed
# EXPOSE 8000

# Run the MCP server
CMD ["python3", "secure_note_mcp.py"]
