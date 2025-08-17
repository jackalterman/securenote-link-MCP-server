# Use a glibc-based Python Image
FROM python:3.13.7-slim

# Set environment variables for Python behavior
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Create and switch to a non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser

# Copy dependency file first (for better build caching)
COPY --chown=appuser:appuser requirements.txt ./ 

# Install only required Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code into container
COPY --chown=appuser:appuser . .

# Ensure setup script is executable and run it
RUN chmod +x setup_mcp.sh && ./setup_mcp.sh

# Expose ports if your app needs it (optional)
# EXPOSE 8000

# Run the MCP server
CMD ["python3", "secure_note_mcp.py"]
