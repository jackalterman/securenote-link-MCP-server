# Secure Notes MCP Server

This is a Model Context Protocol (MCP) server that provides tools for encrypting, sending, and decrypting secrets using the securenote.link API. A burn-after-reading message service with end-to-end encryption.

The agentic process for sending burn-after-reading secure notes can be seamlessly integrated into workflows of all types—whether automated scripts, team collaboration tools, or AI-driven assistants. This enables secure, ephemeral sharing of sensitive information as part of larger business, development, or personal processes.

---

## Features

- 🔐 **Encrypt and Send Secrets**: Encrypt messages and send them to your secure notes API
- 🔓 **Retrieve and Decrypt Secrets**: Retrieve and decrypt secrets from the API
- 🔍 **API Health Check**: Check if your secure notes API is running
- 🛡️ **Password Protection**: Optional password protection for additional security
- 🧰 **Flexible Sharing**: Choose between maximum security (separate key/URL) or convenience (all-in-one link)
- 📝 **Manual Decryption**: Decrypt secrets yourself with a provided Python function

---

## Example: Integrating Secure Notes in an Agentic Workflow

Suppose you use a workflow automation tool like n8n, Make, or a custom AI agent. You can add a step to securely deliver credentials, API keys, or sensitive instructions to a human or another agent, ensuring the information is only accessible once and then self-destructs.

**Sample n8n Workflow (Pseudocode):**

```yaml
- trigger: Onboarding Request Received
- step: Generate API Key
- step: Call Secure Notes MCP Tool
    function: send_secure_note_return_api_url_and_key
    args:
      message: "Your API key: {{ $json.apiKey }}"
      expires_in: 24
- step: Send Email
    to: "newuser@example.com"
    subject: "Your Secure API Key"
    body: |
      Please retrieve your API key using the following secure link:
      {{ $json.retrieval_url }}
      Decryption Key: {{ $json.decryption_key }}
      (This message will self-destruct after being read or after 24 hours.)
```

This approach can be adapted to any agentic or automation platform that supports calling external tools or scripts, enabling secure, ephemeral delivery of secrets as part of your workflow.

---

# Creative Uses for the Secure Note Tool

Beyond its primary use for sending passwords, the secure note tool can be adapted for a variety of creative and practical purposes.

## 1. Developer Secrets & API Keys
Securely share API keys, database connection strings, and other sensitive developer credentials with team members. The automatic expiration prevents credentials from being exposed indefinitely.

## 2. Digital Time Capsule
Write a letter to your future self, encrypt it, and set an expiration date. Save the link and open it when the time comes for a surprise message from your past self.

## 3. "Burn After Reading" Messages
Send one-time instructions, a surprise message, or a secret that you want to be read only once. The self-destructing nature of the notes is perfect for messages you don't want lingering.

## 4. Collaborative Fiction or Games
Start a story, encrypt it, and send the link to a friend to continue it. This can also be used to create a digital scavenger hunt, where each note contains a clue to the next.

## 5. Secure Personal Diary
Keep a private journal where you are the only one with the decryption key. The expiration feature can be used for "disappearing thoughts."

## 6. Anonymous Suggestion Box
Allow team members or individuals in an organization to submit anonymous feedback or ideas by sending an encrypted link to management.

## 7. Secure File Transfer Information
Instead of emailing a sensitive file, upload it to cloud storage and send the shareable link and password via a secure note. This separates the access information from the file's location.

## 8. Emergency Information Kit
Create a note with vital information (e.g., location of a will, emergency contacts, important account identifiers) for a trusted person. Share the link and key for them to use only in an emergency.

## 9. Secret Santa or Gift Exchange
Organize a Secret Santa or gift exchange by sending anonymous assignments or clues via secure notes. The sender remains hidden, and the message self-destructs after being read.

## 10. Temporary Access Codes or Links
Share temporary access codes, meeting links, or event invitations that should only be used once or within a limited time window. The note will expire or self-destruct, reducing the risk of unwanted sharing.


## Prerequisites

- Python 3.10 or higher
- Your secure notes server running (Firebase, in-memory, or cloud)
- The [cryptography](https://cryptography.io/en/latest/) Python library (installed automatically by setup)

---

## Quick Setup

You can use the Secure Notes MCP server in two main ways:

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
docker build -t secure-notes-mcp .
```

#### Run the Docker Container

```bash
docker run --rm -it \
  -v /ABSOLUTE/PATH/TO/your/config:/app/config \
  --name secure-notes-mcp \
  secure-notes-mcp
```
- Mount any config or secrets as needed (optional).

#### Use the Dockerized MCP Server in Claude Desktop or Cursor

- Update your Claude Desktop or Cursor config to use the Docker command as the MCP server:
  ```json
  {
    "mcpServers": {
      "secure-notes": {
        "command": "docker",
        "args": [
          "run", "--rm", "-i", "secure-notes-mcp"
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

### 1. `send_secure_note_return_api_url_and_key`
**Maximum Security (Two-Channel Sharing)**

Encrypts a message, stores it via the API, and returns:
- The API URL to retrieve the encrypted message (returns JSON, not a user-facing page)
- The decryption key (base64-encoded, to be used separately)

**Parameters:**
- `message` (required): The secret message to encrypt
- `password` (optional): Additional password protection
- `expires_in` (optional): Expiration time in hours (1, 24, 72, or 168)

**Returns:**
- Retrieval URL (API endpoint)
- Decryption key (base64-encoded)
- Security notes and usage instructions

**Use Case:**
- Share the URL and key through different channels for maximum security.

---

### 2. `retrieve_and_decrypt_secret`
Retrieves and decrypts a secret from the API.

**Parameters:**
- `secret_id` (required): The ID of the secret to retrieve
- `decryption_key` (required): The decryption key (base64 encoded)
- `password` (optional): Password if the secret is password protected

**Returns:**
- The decrypted message
- Secret ID

**Use Case:**
- Use with the output of `send_secure_note_return_api_url_and_key` for maximum security.

---

### 3. `check_api_health`
Checks if your secure notes API is running and healthy.

**Returns:**
- API health status, server info, uptime, version, and URL

**Use Case:**
- Troubleshoot connectivity or server status.

---

### 4. `send_secure_note`
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
- Share a single link for convenience. Less secure than two-channel sharing.

---

### 5. `get_instructions`
Provides a comprehensive guide on how to use this secure note sharing service, including encryption details, workflows, and tool descriptions.

---

## Use Cases

### Maximum Security (Two-Channel)
1. Call `send_secure_note_return_api_url_and_key()` to get the API URL and decryption key.
2. Share the URL and key through different channels (e.g., email the URL, text the key).
3. The recipient uses `retrieve_and_decrypt_secret()` with the secret ID and key to decrypt the message.

### Convenience (One-Click URL)
1. Call `send_secure_note()` to get a single URL containing both the secret ID and decryption key.
2. Share the URL with the recipient. They can access the message directly.

---

## Security Notes

- 🔑 **Decryption Key**: Never share the decryption key through the same channel as the secret URL for maximum security.
- 🔐 **Password Protection**: Use password protection for additional security.
- ⏰ **Expiration**: Secrets automatically expire based on the set time.
- 🗑️ **One-time Access**: Secrets are deleted after being accessed (unless password protected).
- ⚠️ **One-Click URL**: The decryption key is included in the URL fragment (after `#`). While convenient, this is less secure than sharing the key separately.

---

## Manual Decryption Example (Python)

If you want to decrypt a secret yourself, use the following Python function:

```python
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_message_gcm(encrypted_data: str, key: str, iv: str) -> str:
    """Decrypt a message using AES-256-GCM. Expects base64-encoded ciphertext+tag."""
    key_bytes = base64.b64decode(key)
    iv_bytes = base64.b64decode(iv)
    data = base64.b64decode(encrypted_data)
    if len(key_bytes) != 32:
        raise ValueError("Key must be 32 bytes (256 bits)")
    if len(iv_bytes) != 12:
        raise ValueError("IV must be 12 bytes (96 bits) for GCM")
    if len(data) < 16:
        raise ValueError("Ciphertext too short for GCM tag")
    ciphertext, tag = data[:-16], data[-16:]
    decryptor = Cipher(
        algorithms.AES(key_bytes),
        modes.GCM(iv_bytes, tag),
        backend=default_backend()
    ).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode('utf-8')
```

**How to use:**
1. Fetch the JSON from the API endpoint (see the retrieval URL).
2. Extract `encryptedData` and `iv` from the response.
3. Base64-decode the key, iv, and encryptedData.
4. Call the function above with those values.

---

## Troubleshooting

### API Connection Issues
- Make sure your secure notes server is running.
- Check the `API_BASE_URL` in `secure_note_mcp.py`.
- Use `check_api_health()` to verify connectivity.

### Encryption/Decryption Issues
- Ensure the Python `cryptography` library is installed (run `./setup_mcp.sh` or `pip install -r requirements.txt`).
- The app uses AES-256-GCM for all encryption and decryption. No OpenSSL installation is required.
- If you encounter decryption errors, double-check that you are using the correct base64-encoded key, IV, and encrypted data.

### Claude for Desktop Issues
- Check the Claude logs: `tail -f ~/Library/Logs/Claude/mcp*.log`
- Verify the configuration file syntax.
- Restart Claude for Desktop after configuration changes.

---

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