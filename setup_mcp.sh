#!/bin/bash

echo "🚀 Setting up Secure Notes MCP Server..."

# Check if Python 3.10+ is installed
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if OpenSSL is available
if ! command -v openssl &> /dev/null; then
    echo "⚠️  OpenSSL not found. The server will use Python's secrets module as fallback."
else
    echo "✅ OpenSSL found"
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

# # Test the server
# echo "🧪 Testing the MCP server..."
# python3 secure_note_mcp.py --help 2>/dev/null

# if [ $? -eq 0 ]; then
#     echo "✅ MCP server setup complete!"
#     echo ""
#     echo "📋 Next steps:"
#     echo "1. Update the API_BASE_URL in secure_note_mcp.py if needed"
#     echo "2. Start your secure notes server: node server_firebase.js"
#     echo "3. Run the MCP server: python3 secure_note_mcp.py"
#     echo "4. Configure Claude for Desktop to use this MCP server"
# else
#     echo "❌ MCP server test failed"
#     exit 1
# fi 

echo "🚦 Starting the MCP server..."
python3 secure_note_mcp.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ MCP server started successfully!"
else
    echo "❌ MCP server failed to start. See output above for details."
    exit 1
fi

