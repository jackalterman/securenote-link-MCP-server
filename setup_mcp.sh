#!/bin/bash

echo "🚀 Setting up Secure Notes MCP Server..."

# Check if Python 3.10+ is installed (Alpine/BusyBox compatible)
python_version=$(python3 --version 2>&1 | sed -n 's/Python \([0-9]\+\.[0-9]\+\).*/\1/p')
required_version="3.10"

# Use Python itself for version comparison (more reliable than sort -V in Alpine)
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "✅ Python version: $python_version"
else
    echo "❌ Python 3.10 or higher is required. Current version: $python_version"
    exit 1
fi

# Check if OpenSSL is available
if command -v openssl >/dev/null 2>&1; then
    echo "✅ OpenSSL found"
else
    echo "⚠️  OpenSSL not found. The server will use Python's secrets module as fallback."
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --user

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Start the MCP server
echo "🚦 Starting the MCP server..."
python3 secure_note_mcp.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ MCP server started successfully!"
else
    echo "❌ MCP server failed to start. See output above for details."
    exit 1
fi