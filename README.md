# SecureNote.link MCP Server

<div align="center">

🔐 **Secure, End-to-End Encrypted Note Sharing for AI Agents**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

🌐 **[Try SecureNote.link in your browser](https://securenote.link)**

</div>

## Overview

A Model Context Protocol (MCP) server that enables AI agents to securely share sensitive information through end-to-end encrypted notes. Perfect for Claude Desktop, Cursor, and other MCP-compatible applications where AI agents need to handle confidential data safely.

### Key Features

- 🔐 **Military-Grade Encryption**: AES-256-GCM with client-side encryption
- 📤 **Flexible Sharing**: Choose between convenience (one-click URLs) or maximum security (separate URL + key)
- 🔥 **Burn-After-Reading**: Automatic deletion after viewing
- ⏰ **Customizable Expiration**: 1, 24, 72, or 168 hours
- 🛡️ **Password Protection**: Optional additional security layer
- 🤖 **AI Agent Ready**: Seamless integration with Claude Desktop, Cursor, and more
- 🔍 **Health Monitoring**: Built-in API status checking
- 🧰 **Developer Friendly**: Comprehensive documentation and manual decryption functions

## Quick Start

### Prerequisites

- Python 3.11 or higher
- An MCP-compatible client (Claude Desktop, Cursor, etc.)

### Installation

1. **Download the MCP server file** (save as `secure_note_mcp.py`)

2. **Install dependencies**:
   ```bash
   pip install fastmcp httpx cryptography
   ```

3. **Configure your MCP client** (see detailed instructions below)

4. **Start using secure notes** with your AI agent!

## Setup Instructions

### Claude Desktop

1. **Locate your config file**:
   
   | Platform | Path |
   |----------|------|
   | macOS/Linux | `~/Library/Application Support/Claude/claude_desktop_config.json` |
   | Windows | `%AppData%\Claude\claude_desktop_config.json` |

2. **Add the MCP server configuration**:
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
   > ⚠️ **Important**: Replace `/ABSOLUTE/PATH/TO/secure_note_mcp.py` with the full path to your script

3. **Restart Claude Desktop**

### Cursor

Add the MCP server in your client settings:
```bash
python3 /ABSOLUTE/PATH/TO/secure_note_mcp.py
```

### Docker Deployment

For containerized deployment or better isolation:

1. **Build the image**:
   ```bash
   docker build -t securenote-link-mcp .
   ```

2. **Run the container**:
   ```bash
   docker run --rm -it \
     --name securenote-link-mcp \
     securenote-link-mcp
   ```

3. **Update MCP client config**:
   ```json
   {
     "mcpServers": {
       "securenote.link": {
         "command": "docker",
         "args": ["run", "--rm", "-i", "securenote-link-mcp"]
       }
     }
   }
   ```

## Usage Guide

### Security Models

#### 🟢 Convenient Sharing (One-Click URLs)
- **Best for**: Quick sharing with trusted recipients
- **How it works**: Single URL contains both secret ID and decryption key
- **Security**: Good for most use cases, relies on URL security

#### 🔴 Maximum Security (Two-Channel)
- **Best for**: Highly sensitive information
- **How it works**: Separate URL and decryption key for different communication channels
- **Security**: Highest level - even if one channel is compromised, data remains secure

### Common Workflows

#### Share a Secret with AI Agent
```
You: "Please create a secure note with my API key: sk-1234567890"
Claude: *Uses send_secure_note tool*
Claude: "I've created a secure note that expires in 24 hours: 
https://securenote.link?id=abc123#dGVzdGtleQ=="
```

#### Maximum Security Transfer
```
You: "Create a secure note for my database password, but give me the URL and key separately"
Claude: *Uses send_secure_note_return_api_url_and_key tool*
Claude: "Here's your retrieval URL: https://securenote.link/api/v1/secrets/xyz789
And your decryption key: dGVzdGtleQ=="
```

#### Retrieve and Decrypt a Secret
```
You: "Can you retrieve the secret with ID 'xyz789' using key 'dGVzdGtleQ=='?"
Claude: *Uses retrieve_and_decrypt_secret tool*
Claude: "Successfully decrypted! The message is: 'Your database password here'"
```

## API Reference

### `send_secure_note`
Creates a convenient one-click shareable URL (recommended for most use cases).

**Parameters:**
- `message` (string, required): The secret message to encrypt
- `password` (string, optional): Additional password protection
- `expires_in` (integer, optional): Expiration time in hours (1, 24, 72, or 168) - defaults to 24

**Returns:** 
- Single shareable URL with embedded decryption key in URL fragment
- Format: `https://securenote.link?id={secret_id}#{decryption_key}`

**Security Note:** Key is in URL fragment (after `#`) - not sent to server but may appear in browser history.

### `send_secure_note_return_api_url_and_key`
Creates separate URL and decryption key for maximum security.

**Parameters:**
- `message` (string, required): The secret message to encrypt
- `password` (string, optional): Additional password protection  
- `expires_in` (integer, optional): Expiration time in hours (1, 24, 72, or 168) - defaults to 24

**Returns:** 
- API retrieval URL: `https://securenote.link/api/v1/secrets/{secret_id}`
- Base64-encoded decryption key (separate from URL)

**Security Note:** Share URL and key through different channels for maximum security.

### `retrieve_and_decrypt_secret`
Retrieves and decrypts a secret using ID and key.

**Parameters:**
- `secret_id` (string, required): The secret identifier from the API URL
- `decryption_key` (string, required): Base64-encoded decryption key
- `password` (string, optional): Password if secret is password-protected

**Returns:** 
- Decrypted message content
- Confirmation of secret ID

**Note:** This tool handles password-protected secrets automatically by prompting for verification.

### `check_api_health`
Checks API server status and connectivity.

**Returns:** 
- Health status (OK/Error)
- Server uptime and version information
- API base URL confirmation

**Use Case:** Troubleshooting connection issues or verifying service availability.

### `get_instructions`
Provides comprehensive usage documentation and technical details.

**Returns:** 
- Detailed encryption specifications (AES-256-GCM)
- Workflow explanations and security considerations
- Complete tool documentation

**Use Case:** Getting help or understanding the service's technical implementation.

## Security Details

### Encryption
- **Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Size**: 256 bits (32 bytes) - cryptographically secure random generation
- **IV (Initialization Vector)**: 96 bits (12 bytes) - unique for each encryption
- **Authentication Tag**: 128 bits (16 bytes) - ensures data integrity and authenticity
- **Implementation**: Uses Python's `cryptography` library with `secrets` module for secure randomness

### Data Handling
- **Zero-Knowledge Architecture**: Server never sees unencrypted data or decryption keys
- **Client-Side Encryption**: All encryption/decryption happens on the client
- **Automatic Deletion**: Secrets are deleted after viewing or expiration (burn-after-reading)
- **No Key Storage**: Decryption keys are never stored server-side
- **Secure Transport**: All API communications use HTTPS

### Key Management
- **Key Generation**: Uses `secrets.token_bytes(32)` for cryptographically secure 256-bit keys
- **Key Format**: Base64-encoded for safe transmission and storage
- **Key Separation**: In maximum security mode, keys are completely separate from URLs

### Best Practices
- Use maximum security mode for highly sensitive data
- Set appropriate expiration times
- Consider password protection for additional security
- Share URLs and keys through different channels when possible

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'fastmcp'" or similar**
```bash
pip install fastmcp httpx cryptography
```

**"Command not found" errors**
- Ensure Python 3.11+ is installed: `python3 --version`
- Use the full path to your Python executable if needed: `which python3`
- Check that the MCP server script path is absolute and correct

**Connection or API issues**
- Use the `check_api_health` tool to verify server connectivity
- Check your internet connection and firewall settings
- Ensure https://securenote.link is accessible from your network
- Verify the API_BASE_URL in the script matches the service endpoint

**Encryption/Decryption errors**
- Ensure secret hasn't expired (check expiration time)
- Verify decryption key is complete and hasn't been truncated
- Check that password (if used) is correct
- Secret may have been already viewed (burn-after-reading)

**MCP Configuration issues**
- Restart your MCP client after configuration changes
- Check JSON syntax in configuration files
- Ensure file paths use forward slashes or proper escaping
- Verify script has execute permissions: `chmod +x secure_note_mcp.py`

### Getting Help

1. Use the `get_instructions` tool within your MCP client
2. Check the API health with `check_api_health`
3. Verify your configuration matches the examples above

## Technical Architecture

### How It Works

1. **Client-Side Encryption**
   - Generate 256-bit AES key and 96-bit IV using cryptographically secure random numbers
   - Encrypt message using AES-256-GCM (provides both confidentiality and authenticity)
   - Base64-encode encrypted data, IV, and authentication tag for safe transmission

2. **Server Storage**
   - Send encrypted data + IV to SecureNote.link API (key is never transmitted)
   - Server stores encrypted data with expiration metadata
   - Returns unique secret ID for retrieval

3. **Secure Sharing**
   - **Convenient mode**: Embed decryption key in URL fragment (`#key`)
   - **Maximum security mode**: Provide API URL and key separately

4. **Retrieval & Decryption**
   - Fetch encrypted data from server using secret ID
   - Decrypt locally using provided key and IV
   - Automatically delete secret after viewing (burn-after-reading)

### Security Model

The security relies on:
- **Strong encryption**: AES-256-GCM with authenticated encryption
- **Key separation**: Decryption keys never stored on server
- **Secure randomness**: Cryptographically secure key/IV generation
- **Zero-knowledge**: Server cannot decrypt data without the key
- **Automatic cleanup**: Secrets expire and are deleted after viewing

### API Endpoints

The MCP server communicates with these SecureNote.link API endpoints:

- `POST /api/v1/secrets` - Store encrypted secret
- `GET /api/v1/secrets/{id}` - Retrieve encrypted secret
- `POST /api/v1/secrets/{id}/verify` - Verify password for protected secrets
- `GET /api/v1/health` - Check API health status

## License

MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for secure AI agent workflows**

[Website](https://securenote.link) • [Issues](https://github.com/your-repo/issues) • [Documentation](https://docs.securenote.link)

</div>