# 🔐 SecureNote.link MCP Server

<div align="center">

### **End-to-End Encrypted Note Sharing for AI Agents**

*Because your secrets deserve better than plain text*

[![MCP Hub](https://img.shields.io/badge/MCP%20Hub-Available-brightgreen?logo=docker&logoColor=white)](https://hub.docker.com/mcp/server/securenote-link-mcp-server/overview)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-5C5CFF)](https://modelcontextprotocol.io/)

[Try the Web App](https://securenote.link) • [MCP Hub](https://hub.docker.com/mcp/server/securenote-link-mcp-server/overview) • [Report Issue](https://github.com/your-repo/issues)

</div>

---

## 🎯 What is This?

Ever needed your AI assistant to share sensitive information with you securely? API keys, passwords, database credentials, or any secret data? **SecureNote.link MCP Server** lets Claude, Cursor, and other AI agents create encrypted notes that **you can safely open in your browser**.

Your AI creates the note, gives you a link, and you open it at **[securenote.link](https://securenote.link)**—where the note decrypts in your browser and then self-destructs. Think of it as a **secure handoff** from AI to human, with military-grade encryption and zero-knowledge architecture that ensures even the server never sees your data.

> ### 🌐 For Recipients: Reading Secure Notes
> 
> **Someone sent you a secure note link?** Visit **[securenote.link](https://securenote.link)** in any browser!
> 
> - **One-click links** → Just click and read (note auto-decrypts)
> - **Two-part security** → Paste the URL and key into a browser (separated by #)
> - **Works everywhere** → Desktop, mobile, any browser
> - **No sign-up needed** → Completely anonymous

---

## ✨ Why You'll Love It

<table>
<tr>
<td width="50%">

### 🛡️ **Fort Knox Security**
- **AES-256-GCM encryption** (the same used by governments)
- **Zero-knowledge architecture** (server never sees your data)
- **Client-side encryption** (your data is encrypted before leaving your device)
- Optional **password protection** for extra peace of mind

</td>
<td width="50%">

### ⚡ **Ridiculously Easy**
- **One-click sharing** for recipients (just click the link!)
- **Works in any browser** via [securenote.link](https://securenote.link)
- **No account needed** for you or recipients
- Works with **Claude Desktop, Cursor**, and any MCP client

</td>
</tr>
<tr>
<td width="50%">

### ⏱️ **Flexible & Smart**
- Set expiration: **1, 24, 72, or 168 hours**
- **Self-destructing notes** that vanish after first view
- **Health monitoring** to verify everything's working
- **Manual decryption** functions for advanced users

</td>
<td width="50%">

### 🧑‍💻 **Developer Friendly**
- Clean, documented API
- Comprehensive error handling
- Built-in usage instructions
- Active maintenance and support

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Installation

**Option 1: MCP Hub (Recommended)** 🐳

Available as a pre-built Docker image on MCP Hub:

👉 **[Get it on MCP Hub](https://hub.docker.com/mcp/server/securenote-link-mcp-server/overview)**

Follow the simple setup instructions on MCP Hub to add it to your Claude Desktop or other MCP client.

---

**Option 2: Direct Python Installation** 🐍

```bash
# Install dependencies
pip install -r requirements.txt

```

<details>
<summary><b>📋 Claude Desktop Configuration</b></summary>

1. **Find your config file:**
   - **macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%AppData%\Claude\claude_desktop_config.json`

2. **Add this configuration:**
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

3. **Restart Claude Desktop** and you're ready!

</details>

---

## 🎨 How It Works

Your AI agent creates an encrypted note, and **you share the link with anyone who needs the information**. They simply open it in their browser at **[securenote.link](https://securenote.link)** to read it.

### Two Security Modes for Different Needs

#### 🟢 **Convenience Mode** (One-Click URLs)
Perfect for quick, trusted sharing. Recipients just click and read—no copy-pasting required!

```
https://securenote.link?id=abc123#dGVzdGtleQ==
                                 ↑
                    Decryption key in URL fragment
                    (never sent to server!)
```

**How it works:**
1. AI creates the encrypted note
2. You get a single link
3. Share via email, Slack, chat, etc.
4. Recipient clicks → note decrypts in their browser → self-destructs

**Best for:** Team members, trusted colleagues, or when convenience matters

---

#### 🔴 **Maximum Security Mode** (Two-Channel)
For when security is paramount. Get separate URL and decryption key to share through different channels.

```
URL:  https://securenote.link/api/v1/secrets/xyz789
Key:  dGVzdGtleQ==
      ↑
  Share these via different channels!
```

**How it works:**
1. AI creates the encrypted note  
2. You get URL + separate decryption key
3. Share URL via one channel (email)
4. Share key via another channel (text/Slack)
5. Recipient pastes both into securenote.link → decrypts

**Best for:** Highly sensitive data, compliance requirements, paranoid security posture

---

### 🤖 Can AI Agents Share with Other AI Agents?

Yes! The `retrieve_and_decrypt_secret` tool allows one AI agent to retrieve notes created by another. However, this is less common since AI agents typically don't have persistent memory across conversations. The primary use case is **AI-to-human** sharing.

---

## 💡 Real-World Examples

### 📧 Email Credentials Securely

```
You: "Generate our new email server password and create a secure note 
      I can send to the IT team."

Claude: "I've generated a strong password and created a secure note:
         
         🔗 https://securenote.link?id=x7k2p#dGVzdGtleQ==
         
         Share this link via email or Slack. It expires in 24 hours
         and self-destructs after the first person views it.
         
         They just click the link and the password will appear in their browser!"
```

---

### 🔐 Share API Keys with Team Members

```
You: "Create a secure note with our production API key 
      that I can share with the new developer."

Claude: "Created a secure note with your API key:
         
         🔗 https://securenote.link?id=k9m3x#c2VjcmV0a2V5
         
         Send this link to your developer. When they click it:
         • The note will decrypt in their browser
         • They can copy the API key
         • The note will immediately delete itself
         
         No chat logs, no email archives—completely secure!"
```

---

### 🛡️ Maximum Security for Sensitive Data

```
You: "I need to share database credentials with our contractor,
      but I want maximum security."

Claude: "Created a secure note with two-channel security:
         
         📎 Send via email: 
         https://securenote.link/api/v1/secrets/9m4x2
         
         🔑 Send via Slack/text: 
         dGVzdGtleXZhbHVl
         
         They'll need BOTH to decrypt. Share them through different
         channels—even if one is compromised, the data stays secure.
         
         They can paste both into securenote.link to retrieve the credentials!"
```

---

### 🔍 Retrieve and Read a Note (as a Human)

When someone sends you a secure note link:

1. **Click the link** → Opens securenote.link in your browser
2. **Note decrypts automatically** → See the secret message
3. **Copy what you need** → Message deletes immediately after viewing
4. **Done!** → No trace left behind

Or if you have a separate URL and key:
1. **Construct the full URL** by combining them:
   - Format: `https://securenote.link?id={secret_id}#{decryption_key}`
   - Example: `https://securenote.link?id=xyz789#dGVzdGtleQ==`
2. **Open the assembled URL** in your browser
3. Secret decrypts automatically and is then deleted

---

## 🔧 Available Tools

The MCP server provides these tools to your AI agent:

| Tool | What It Does |
|------|--------------|
| `send_secure_note` | Create a convenient one-click shareable URL |
| `send_secure_note_return_api_url_and_key` | Create separate URL + key for maximum security |
| `retrieve_and_decrypt_secret` | Retrieve and decrypt a secret using ID and key |
| `check_api_health` | Verify API server status and connectivity |
| `get_instructions` | Get comprehensive usage documentation |

<details>
<summary><b>📖 Full API Reference</b></summary>

### `send_secure_note`
Creates a convenient one-click URL (recommended for most use cases).

**Parameters:**
- `message` (string, required): The secret message to encrypt
- `password` (string, optional): Additional password protection
- `expires_in` (integer, optional): Hours until expiration (1, 24, 72, or 168)

**Returns:** Single shareable URL with embedded decryption key

---

### `send_secure_note_return_api_url_and_key`
Creates separate URL and key for maximum security.

**Parameters:**
- `message` (string, required): The secret message to encrypt
- `password` (string, optional): Additional password protection
- `expires_in` (integer, optional): Hours until expiration (1, 24, 72, or 168)

**Returns:** API URL and Base64-encoded decryption key (separately)

---

### `retrieve_and_decrypt_secret`
Retrieves and decrypts a secret.

**Parameters:**
- `secret_id` (string, required): Secret identifier
- `decryption_key` (string, required): Base64-encoded key
- `password` (string, optional): If the secret is password-protected

**Returns:** Decrypted message content

</details>

---

## 🔬 Security Deep-Dive

### The Encryption

- **Algorithm:** AES-256-GCM (Galois/Counter Mode)
  - 256-bit keys (impossible to brute force with current technology)
  - Authenticated encryption (integrity + confidentiality)
  - Unique IV for each message (prevents pattern analysis)

### The Architecture

```
┌─────────────┐                    ┌─────────────┐
│   Client    │                    │   Server    │
│  (Your AI)  │                    │             │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │ 1. Generate random key           │
       │    (never sent!)                 │
       │                                  │
       │ 2. Encrypt message locally       │
       │────────────────────────────────> │
       │    (only encrypted data sent)    │
       │                                  │
       │ 3. Server stores encrypted blob  │
       │    (can't decrypt without key!)  │
       │                                  │
       │ 4. Returns secret ID             │
       │ <──────────────────────────────  │
       │                                  │
       
Key stays with client → Zero-knowledge achieved ✅
```

### Why This Matters

1. **Zero-Knowledge:** The server literally cannot decrypt your data (it doesn't have the key)
2. **No Trust Required:** You don't need to trust the server operator
3. **Self-Destructing:** Even if someone gets the URL, the note deletes after viewing
4. **Time-Limited:** Secrets automatically expire, reducing exposure window

---

## 🆘 Troubleshooting

<details>
<summary><b>❌ Module not found errors</b></summary>

```bash
pip install fastmcp httpx cryptography
```

Make sure you're using Python 3.11+:
```bash
python3 --version
```

</details>

<details>
<summary><b>🔌 Connection issues</b></summary>

Use the built-in health check:
```
Ask your AI: "Check the SecureNote.link API health"
```

Verify:
- Internet connection is working
- https://securenote.link is accessible
- Firewall isn't blocking the connection

</details>

<details>
<summary><b>🔓 Decryption failures</b></summary>

Common causes:
- Secret has already been viewed (burn-after-reading)
- Secret has expired (check expiration time)
- Wrong decryption key or password
- Key was truncated when copying

</details>

<details>
<summary><b>⚙️ MCP configuration problems</b></summary>

- Restart your MCP client after config changes
- Verify JSON syntax is valid
- Use absolute paths (not relative)
- Check file permissions on the script

</details>

---

## 🤝 Contributing & Support

Found a bug? Have a feature request? We'd love to hear from you!

- **Issues:** [Report on GitHub](https://github.com/your-repo/issues)
- **Discussions:** Share ideas and get help
- **Documentation:** [Full docs available](https://docs.securenote.link)

---

## 📄 License

MIT License - Use it however you want!

---

<div align="center">

### Made with ❤️ for secure AI workflows

**Your secrets are safe with us (because we never see them!)**

[🌐 Try SecureNote.link](https://securenote.link) • [🐳 Get on MCP Hub](https://hub.docker.com/mcp/server/securenote-link-mcp-server/overview)

⭐ **Star us on GitHub if this helps you!**

</div>
