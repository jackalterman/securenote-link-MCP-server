# Secure Notes MCP Server

This is a Model Context Protocol (MCP) server that provides tools for encrypting, sending, and decrypting secrets using your secure notes API.

## Features

- 🔐 **Encrypt and Send Secrets**: Encrypt messages and send them to your secure notes API
- 🔓 **Retrieve and Decrypt Secrets**: Retrieve and decrypt secrets from the API
- 🔍 **API Health Check**: Check if your secure notes API is running
- 📊 **Admin Status**: Get information about stored secrets
- 🛡️ **Password Protection**: Optional password protection for additional security

## Prerequisites

- Python 3.10 or higher
- Your secure notes server running (Firebase or in-memory)
- OpenSSL (optional, will fallback to Python's secrets module)

## Quick Setup

1. **Install dependencies:**
   ```bash
   chmod +x setup_mcp.sh
   ./setup_mcp.sh
   ```

2. **Update the API URL** in `mcp.py`:
   ```python
   API_BASE_URL = "http://your-server-ip:3000"  # Update this
   ```

3. **Start your secure notes server:**
   ```bash
   node server_firebase.js
   # or
   node server_in_memory.js
   ```

4. **Test the MCP server:**
   ```bash
   python3 mcp.py
   ```

## Available Tools

### 1. `encrypt_and_send_secret`
Encrypts a message and sends it to your secure notes API.

**Parameters:**
- `message` (required): The secret message to encrypt
- `password` (optional): Additional password protection
- `expires_in` (optional): Expiration time in hours (1, 24, 72, or 168)

**Example:**
```
encrypt_and_send_secret("My secret message", "optional_password", 24)
```

### 2. `retrieve_and_decrypt_secret`
Retrieves and decrypts a secret from the API.

**Parameters:**
- `secret_id` (required): The ID of the secret to retrieve
- `decryption_key` (required): The decryption key (base64 encoded)
- `password` (optional): Password if the secret is password protected

**Example:**
```
retrieve_and_decrypt_secret("a1b2c3d4e5f678901234567890123456", "base64_key_here", "optional_password")
```

### 3. `check_api_health`
Checks if your secure notes API is running and healthy.

**Example:**
```
check_api_health()
```

### 4. `get_admin_status`
Gets admin status information about stored secrets.

**Example:**
```
get_admin_status()
```

### 5. `generate_secret_url`
Generates a URL to retrieve a secret message by its ID.

**Parameters:**
- `secret_id` (required): The ID of the secret to generate a URL for (32-character hexadecimal string)

**Example:**
```
generate_secret_url("a1b2c3d4e5f678901234567890123456")
```

### 6. `generate_secret_url_with_key`
Generates a URL that includes both the secret ID and the decryption key for convenience (not recommended for secure sharing).

**Parameters:**
- `secret_id` (required): The ID of the secret (32-character hexadecimal string)
- `decryption_key` (required): The decryption key (base64 encoded)

**Example:**
```
generate_secret_url_with_key("a1b2c3d4e5f678901234567890123456", "base64_key_here")
```

## Claude for Desktop Configuration

To use this MCP server with Claude for Desktop:

1. **Open Claude for Desktop configuration:**
   ```bash
   # macOS/Linux
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   code $env:AppData\Claude\claude_desktop_config.json
   ```

2. **Add the MCP server configuration:**
   ```json
   {
     "mcpServers": {
       "secure-notes": {
         "command": "python3",
         "args": ["/ABSOLUTE/PATH/TO/mcp.py"]
       }
     }
   }
   ```

3. **Restart Claude for Desktop**

## Usage Examples

### Encrypt and Send a Secret
```
User: "I want to send a secret message to my friend"
Claude: I'll help you encrypt and send a secret message. Let me use the encrypt_and_send_secret tool.

[Claude uses the tool]
encrypt_and_send_secret("This is my secret message for my friend", null, 24)

Result: ✅ Secret successfully encrypted and sent!

🔑 Secret ID: a1b2c3d4e5f678901234567890123456
🔐 Password Protected: false
⏰ Expires In: 24 hours

🔑 Decryption Key (keep this secret!):
base64_encoded_key_here

📋 Share with recipient:
- URL: http://192.168.86.132:3000/api/secrets/a1b2c3d4e5f678901234567890123456
- Decryption Key: base64_encoded_key_here

⚠️ Important: The recipient needs BOTH the URL and the decryption key to decrypt the message.
```

### Retrieve and Decrypt a Secret
```
User: "I received a secret with ID a1b2c3d4e5f678901234567890123456 and key base64_key_here"
Claude: I'll help you retrieve and decrypt that secret. Let me use the retrieve_and_decrypt_secret tool.

[Claude uses the tool]
retrieve_and_decrypt_secret("a1b2c3d4e5f678901234567890123456", "base64_key_here", null)

Result: ✅ Secret successfully decrypted!

📝 Message:
This is my secret message for my friend

🔑 Secret ID: a1b2c3d4e5f678901234567890123456
```

## Security Notes

- 🔑 **Decryption Key**: Never share the decryption key through the same channel as the secret URL
- 🔐 **Password Protection**: Use password protection for additional security
- ⏰ **Expiration**: Secrets automatically expire based on the set time
- 🗑️ **One-time Access**: Secrets are deleted after being accessed (unless password protected)

## Troubleshooting

### API Connection Issues
- Make sure your secure notes server is running
- Check the `API_BASE_URL` in `mcp.py`
- Use `check_api_health()` to verify connectivity

### Encryption/Decryption Issues
- Ensure OpenSSL is installed for best performance
- The server will fallback to Python's secrets module if OpenSSL is unavailable

### Claude for Desktop Issues
- Check the Claude logs: `tail -f ~/Library/Logs/Claude/mcp*.log`
- Verify the configuration file syntax
- Restart Claude for Desktop after configuration changes

## Development

The MCP server follows the [Model Context Protocol specification](https://modelcontextprotocol.io/quickstart/server) and uses the FastMCP framework for easy tool development.

### Adding New Tools

To add a new tool, use the `@mcp.tool()` decorator:

```python
@mcp.tool()
async def my_new_tool(param1: str, param2: int) -> str:
    """Description of what this tool does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
    """
    # Tool implementation
    return "Result"
```

The FastMCP framework automatically generates tool definitions from Python type hints and docstrings. 