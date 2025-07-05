# Use a glibc-based Python 3.14 image (beta)
FROM python:3.11-slim


# Set environment variables
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /

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
