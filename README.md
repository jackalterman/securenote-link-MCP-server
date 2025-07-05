# SecureNote.link MCP Server

🌐 [securenote.link](https://securenote.link) - Try the secure note sharing service in your browser!

A Model Context Protocol (MCP) server that provides secure, end-to-end encrypted note sharing capabilities. This server integrates with Claude Desktop, Cursor, and other MCP-compatible applications to enable AI agents to securely share sensitive information.

## Features

- 🔐 **End-to-End Encryption**: AES-256-GCM encryption ensures your secrets stay private
- 📤 **Secure Message Sharing**: Send encrypted messages with customizable expiration times (1, 24, 72, or 168 hours)
- 🔥 **Burn-After-Reading**: Secrets are automatically deleted after being viewed once
- 🔓 **Two Sharing Modes**: 
  - **Convenient**: Single-click URLs for quick sharing
  - **Maximum Security**: Separate URL and decryption key for sensitive data
- 🛡️ **Password Protection**: Add an extra layer of security with optional passwords
- 🔍 **API Health Monitoring**: Check server status and connectivity
- 🧰 **Flexible Integration**: Use as an MCP server or integrate with your own applications
- 📝 **Developer Friendly**: Includes manual decryption functions and detailed documentation
- 🤖 **Agentic Workflows**: Endless possibilities for AI agents to securely share and retrieve sensitive information

---


## Prerequisites

- Python 3.11 or higher
- The [cryptography](https://cryptography.io/en/latest/) Python library (installed automatically by setup)

---

## Quick Setup

### 1. Add the MCP Server to Claude Desktop or Cursor

#### Claude Desktop

1. **Find your Claude Desktop config file:**
   - **macOS/Linux:**
     ```bash
     code ~/Library/Application\ Support/Claude/claude_desktop_config.json
     ```
   - **Windows:**
     ```powershell
     code $env:AppData\Claude\claude_desktop_config.json
     ```

2. **Add the MCP server configuration:**
   ```json
   {
     "mcpServers": {
       "secure-notes": {
         "command": "python3",
         "args": ["/ABSOLUTE/PATH/TO/secure_note_mcp.py"]
       }
     }
   }
   ```
   - Replace `/ABSOLUTE/PATH/TO/secure_note_mcp.py` with the full path to your script.

3. **Restart Claude Desktop** to apply the changes.

#### Cursor (or other MCP-compatible clients)

- Add the MCP server in your client's settings, using the command:
  ```bash
  python3 /ABSOLUTE/PATH/TO/secure_note_mcp.py
  ```
- Or, if the client supports a GUI, add a new MCP server and point it to the script above.

---

### 2. Build and Run with Docker

You can run the MCP server in a Docker container for easy deployment and isolation.

#### Build the Docker Image

```bash
docker build -t securenote-link-mcp .
```

#### Run the Docker Container

```bash
docker run --rm -it \
  -v /ABSOLUTE/PATH/TO/your/config:/app/config \
  --name securenote-link-mcp \
  securenote-link-mcp
```
- Mount any config or secrets as needed (optional).

#### Use the Dockerized MCP Server in Claude Desktop or Cursor

- Update your Claude Desktop or Cursor config to use the Docker command as the MCP server:
  ```json
  {
    "mcpServers": {
      "securenote.link": {
        "command": "docker",
        "args": [
          "run", "--rm", "-i", "securenote-link-mcp"
        ]
      }
    }
  }
  ```
  - This will launch the MCP server in a container each time it's needed.
  - Make sure Docker is running and the image is built.

---

**Choose the method that best fits your workflow!**
- For local development, running the Python script directly is easiest.
- For isolation, reproducibility, or server environments, Docker is recommended.

---

## Tool Reference

### 1. `send_secure_note`
**Convenience Sharing (One-Click URL)**

Encrypts a message, stores it via the API, and generates a single, shareable URL that embeds both the secret ID and the decryption key.

**Parameters:**
- `message` (required): The secret message to encrypt and send
- `password` (optional): Additional password protection
- `expires_in` (optional): Expiration time in hours (1, 24, 72, or 168)

**Returns:**
- A single URL containing both the secret ID and the decryption key (in the URL fragment)
- Security notes and usage instructions

**Use Case:**
- Share a single link for convenience.

---

### 2. `send_secure_note_return_api_url_and_key`
**Maximum Security Sharing (Two-Channel)**

Encrypts a message, stores it via the API, and returns the retrieval URL and decryption key separately for maximum security.

**Parameters:**
- `message` (required): The secret message to encrypt and send
- `password` (optional): Additional password protection
- `expires_in` (optional): Expiration time in hours (1, 24, 72, or 168)

**Returns:**
- API retrieval URL (returns JSON, not a user-facing page)
- Decryption key (base64-encoded)
- Security notes and usage instructions

**Use Case:**
- Maximum security workflows where you want to share the URL and key through different channels

---

### 3. `retrieve_and_decrypt_secret`
Retrieves and decrypts a secret from the API using the provided secret ID and decryption key.

**Parameters:**
- `secret_id` (required): The ID of the secret to retrieve
- `decryption_key` (required): The decryption key (base64 encoded)
- `password` (optional): Password if the secret is password protected

**Returns:**
- The decrypted message
- Secret ID

**Use Case:**
- Use with the output of `send_secure_note_return_api_url_and_key` for maximum security

---

### 4. `check_api_health`
Checks if your secure notes API is running and healthy.

**Returns:**
- API health status, server info, uptime, version, and URL

**Use Case:**
- Troubleshoot connectivity or server status

---

### 5. `get_instructions`
Provides a comprehensive guide on how to use this secure note sharing service, including encryption details, workflows, and tool descriptions.

**Returns:**
- Detailed documentation covering encryption process, sharing workflows, and tool usage

**Use Case:**
- Get help understanding how to use the service effectively

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**MIT License**

Copyright (c) 2024 SecureNote.link MCP Server

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.