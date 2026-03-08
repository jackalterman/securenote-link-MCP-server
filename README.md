# 🔐 SecureNote.link MCP Server

<div align="center">

### **Give your AI a way to hand you secrets — safely.**

*Encrypted. Self-destructing. Zero-knowledge. Actually fun to use.*

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-5C5CFF)](https://modelcontextprotocol.io/)

[🌐 Open the Web App](https://securenote.link) • [🐛 Report an Issue](https://github.com/your-repo/issues)

</div>

---

## 👋 What's This For?

Picture this: you ask your AI assistant to generate a new password, rotate an API key, or draft some credentials for a teammate. It does — and then it just... types it out in the chat window. In plain text. In your chat history. Sitting there forever.

**SecureNote.link MCP Server fixes that.**

It gives any MCP-compatible AI agent the ability to package a secret into an end-to-end encrypted, self-destructing note and hand you back a link. You click it, you see your secret in the browser, and then it's gone. No plain text in the chat. No server that can read it. No trace.

Think of it as a **secure handoff channel** between your AI agent and the real world.

> ### 📬 Someone sent you a secure note link?
> Just visit **[securenote.link](https://securenote.link)** — no account needed, works in any browser. Click, read, done. The note deletes itself the moment you open it.

---

## ✨ The Good Stuff

| | |
|---|---|
| 🛡️ **AES-256-GCM encryption** | The same algorithm used to protect classified government data. Your note is unreadable without the key — including to the server. |
| 💣 **Self-destructing notes** | Notes are deleted the moment they're read. No second chances, no lingering copies. |
| ⏱️ **Automatic expiry** | Set a note to vanish after 1, 24, 72, or 168 hours — whether it's been read or not. |
| 🔑 **Optional password protection** | Add a password for a second layer of security, shared through a separate channel. |
| 🧠 **Zero-knowledge architecture** | The encryption key is *never* sent to the server. It literally cannot read your data. |

---

## 🚀 Getting Started

### Option 1 — Docker (Recommended) 🐳

The cleanest way to run this. No dependency headaches, no version conflicts.

```bash
# Build the image
docker build -t securenote-mcp .
```

Then point your MCP client at it. See the configuration section below.

---

### Option 2 — Direct Python 🐍

```bash
pip install -r requirements.txt
```

Requires **Python 3.11 or higher**.

---

### Configuring Your MCP Client

1. Find your MCP client config file:
   - **Windows:** `%AppData%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add the server block:

**Python:**
```json
{
  "mcpServers": {
    "securenote": {
      "command": "python3",
      "args": ["C:/absolute/path/to/secure_note_mcp.py"]
    }
  }
}
```

**Docker:**
```json
{
  "mcpServers": {
    "securenote": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "securenote-mcp"]
    }
  }
}
```

3. **Restart your MCP client.** That's it — your AI agent now knows how to create secure notes.

---

## 🎨 How It Works

When you ask your AI agent to create a secure note, here's what actually happens under the hood:

```
1. The AI agent generates a random 256-bit encryption key  ← stays on your side, never uploaded
2. The AI agent encrypts your message with AES-256-GCM
3. Only the encrypted blob is sent to the server
4. The server stores the ciphertext and returns an ID
5. The AI agent combines the ID + key into a shareable URL
6. You click it → your browser decrypts it locally → note is deleted
```

The server never has the key. The server never sees the plaintext. Even if someone broke into the server, they'd find nothing useful.

---

## 🔗 The URL Explained

A secure note URL looks like this:

```
https://securenote.link?id=abc123#dGVzdGtleQ==
                                  ↑
                     Decryption key lives here (the "fragment")
                     Fragments are never sent to the server by browsers
```

The part after `#` is called a URL fragment. Browsers handle it entirely locally — it never travels over the network. That's the clever bit that makes one-click sharing possible without compromising security.

---

## 💡 Real-World Examples

### Sharing a password with a teammate
```
You:      "Generate a strong password for the staging database and
           send it to me as a secure note."

AI Agent: "Done! Here's your secure note:
           🔗 https://securenote.link?id=x7k2p#dGVzdGtleQ==

           It expires in 24 hours and deletes itself after you open it."
```

### Sending credentials to a new developer
```
You:      "Create a secure note with our AWS access keys for the
           new developer starting Monday."

AI Agent: "Created! Send them this link:
           🔗 https://securenote.link?id=k9m3x#c2VjcmV0a2V5

           Once they click it, the keys will appear in their browser
           and the note will self-destruct. Nothing left in the chat."
```

### Maximum security mode
```
You:      "I need to share these database credentials with our contractor
           but I want to be extra careful."

AI Agent: "I've split it into two parts for two-channel delivery:

           📧 Send this via email:
           https://securenote.link?id=9m4x2#dGVzdGtleXZhbHVl

           💬 Send this via text separately:
           password: CorrectHorseBatteryStaple

           They'll need both to read the note. Even if one channel
           is compromised, the data stays safe."
```

---

## 🔧 The Tools

Your AI agent has access to three tools from this server:

### `create_note`
Creates an encrypted note and returns everything you need to share it.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | string | required | The secret message to encrypt |
| `password` | string | optional | Extra password protection |
| `expires_in` | integer | 24 | Hours until auto-deletion: `1`, `24`, `72`, or `168` |

Returns a JSON object with the note `id`, `key`, one-click `url`, `expires_in_hours`, and `password_protected` status.

---

### `get_note`
Fetches and decrypts a note. Useful when an AI agent needs to read back a note it (or another agent) created.

| Parameter | Type | Description |
|---|---|---|
| `secret_id` | string | The note's ID |
| `decryption_key` | string | The base64 key from `create_note` or the URL fragment |
| `password` | string | Only needed if the note is password-protected |

Returns the plain-text message.

---

### `get_instructions`
Returns a quick reference guide for the AI agent — useful for prompting it to explain how the service works or reminding it of the available options.

---

## 🔒 Security At a Glance

| Property | Detail |
|---|---|
| Encryption | AES-256-GCM |
| Key size | 256-bit |
| IV | 96-bit, unique per note |
| Auth tag | 128-bit (integrity + authenticity) |
| Key storage | Never stored on server |
| Note lifetime | Deleted on first read or at expiry |
| Transport | HTTPS only |
| Input limits | Max 100 KB text · Max 1 KB password |

---

## 🆘 Troubleshooting

**"Module not found" errors**
```bash
pip install fastmcp httpx cryptography
```

**"Note not found" when retrieving**
The note was probably already read (they self-destruct on first view), or it expired. Notes are one-shot by design.

**Decryption failed / garbled output**
The key was likely truncated when copying. Make sure you're using the full key from the `key` field in `create_note`'s response, not a manually copied fragment.

**MCP server not showing up in your AI agent**
- Use an absolute path in your config, not a relative one
- Validate your JSON — one missing comma breaks the whole config
- Restart your MCP client fully after any config changes

---

## 📄 License

MIT — use it, fork it, ship it.

---

<div align="center">

**Made for people who believe "just paste it in the chat" isn't good enough.**

[🌐 securenote.link](https://securenote.link)

</div>
