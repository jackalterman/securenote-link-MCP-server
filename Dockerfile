# Use Alpine Linux as the base image
FROM python:3.14.0b3-alpine3.21

# Install bash
RUN apk add --no-cache bash grep

# Set the working directory inside the container
WORKDIR /mcp

# Copy the MCP server code into the container
COPY . .

# Make the setup script executable and run it
RUN chmod +x setup_mcp.sh && ./setup_mcp.sh

# Expose any ports if needed (optional, not strictly required for stdio transport)
# EXPOSE 8000

# Run the MCP server
CMD ["python3", "secure_note_mcp.py"] 