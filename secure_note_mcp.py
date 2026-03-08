from typing import Any, Optional, Tuple
import httpx
import base64
import json
import re
import secrets
import sys
from fastmcp import FastMCP
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Initialize FastMCP server
mcp = FastMCP("securenote.link")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

API_BASE_URL       = "https://securenote.link"
VALID_EXPIRY_HOURS = [1, 24, 72, 168]

# --- Adjustable size limits ---
MAX_TEXT_BYTES     = 100_000   # 100 KB — maximum size of the plaintext message
MAX_PASSWORD_BYTES =   1_024   #   1 KB — maximum size of the password

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def make_api_request(
    method: str,
    endpoint: str,
    data: Optional[dict] = None
) -> Optional[dict[str, Any]]:
    """Make a request to the secure notes API with proper error handling."""
    url     = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json", "x-source": "mcp"}

    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException:
            print(f"API request timed out for {url}", file=sys.stderr)
            return None
        except httpx.HTTPStatusError as e:
            print(
                f"API request failed with status {e.response.status_code}: {e.response.text}",
                file=sys.stderr
            )
            return None
        except Exception as e:
            print(f"API request failed: {e}", file=sys.stderr)
            return None


def _validate_secret_id(secret_id: str) -> bool:
    """Return True only if secret_id is a safe alphanumeric/hyphen/underscore string."""
    return bool(re.fullmatch(r'[A-Za-z0-9\-_]{1,128}', secret_id))


def generate_gcm_key_and_iv() -> Tuple[str, str]:
    """Generate a random 256-bit key and 96-bit IV for AES-GCM, both base64-encoded."""
    key = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')
    iv  = base64.b64encode(secrets.token_bytes(12)).decode('utf-8')
    return key, iv


def encrypt_message_gcm(message: str, key: str, iv: str) -> str:
    """Encrypt a message using AES-256-GCM. Returns base64-encoded ciphertext+tag."""
    if not message:
        raise ValueError("Message cannot be empty")
    key_bytes = base64.b64decode(key)
    iv_bytes  = base64.b64decode(iv)
    if len(key_bytes) != 32:
        raise ValueError("Key must be 32 bytes (256 bits)")
    if len(iv_bytes) != 12:
        raise ValueError("IV must be 12 bytes (96 bits) for GCM")
    encryptor = Cipher(
        algorithms.AES(key_bytes),
        modes.GCM(iv_bytes),
    ).encryptor()
    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(ciphertext + encryptor.tag).decode('utf-8')


def decrypt_message_gcm(encrypted_data: str, key: str, iv: str) -> str:
    """Decrypt a message using AES-256-GCM. Expects base64-encoded ciphertext+tag."""
    key_bytes = base64.b64decode(key)
    iv_bytes  = base64.b64decode(iv)
    data      = base64.b64decode(encrypted_data)
    if len(key_bytes) != 32:
        raise ValueError("Key must be 32 bytes (256 bits)")
    if len(iv_bytes) != 12:
        raise ValueError("IV must be 12 bytes (96 bits) for GCM")
    if len(data) < 16:
        raise ValueError("Ciphertext too short to contain a GCM auth tag")
    ciphertext, tag = data[:-16], data[-16:]
    decryptor = Cipher(
        algorithms.AES(key_bytes),
        modes.GCM(iv_bytes, tag),
    ).decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def create_note(
    text: str,
    password: Optional[str] = None,
    expires_in: int = 24
) -> str:
    """
    Encrypt a message and store it via the securenote.link API.

    Returns the note ID, decryption key, shareable one-click URL, expiry,
    and password-protection status.

    The one-click URL embeds the decryption key in the fragment (#), which is
    never sent to the server. For maximum security, share the URL and key
    through separate channels.

    Args:
        text:       The plain-text message to encrypt and store.
        password:   Optional password for additional protection.
        expires_in: Expiry time in hours — must be one of: 1, 24, 72, 168.
    """
    # --- validate text ---
    if not text or not text.strip():
        return "Error: text cannot be empty."
    if len(text.encode('utf-8')) > MAX_TEXT_BYTES:
        return f"Error: text exceeds the maximum allowed size of {MAX_TEXT_BYTES // 1000} KB."

    # --- validate password ---
    if password is not None:
        if len(password.encode('utf-8')) > MAX_PASSWORD_BYTES:
            return f"Error: password exceeds the maximum allowed size of {MAX_PASSWORD_BYTES} bytes."

    # --- validate expiry ---
    if expires_in not in VALID_EXPIRY_HOURS:
        return f"Error: expires_in must be one of {VALID_EXPIRY_HOURS}."

    try:
        key, iv        = generate_gcm_key_and_iv()
        encrypted_data = encrypt_message_gcm(text.strip(), key, iv)

        api_data: dict = {
            "encryptedData": encrypted_data,
            "iv":            iv,
            "expiresIn":     expires_in,
        }
        if password:
            api_data["password"] = password

        response = await make_api_request("POST", "/api/v1/secrets", api_data)
        if not response:
            return "Error: failed to reach the API. Check that the server is running."

        secret_id = response.get("id")
        if not secret_id:
            return "Error: API did not return a secret ID."

        result = {
            "message":          "Note created successfully.",
            "id":               secret_id,
            "key":              key,
            "url":              f"{API_BASE_URL}?id={secret_id}#{key}",
            "expires_in_hours": response.get("expiresIn", expires_in),
            "password_protected": bool(password),
        }
        return json.dumps(result, indent=2)

    except Exception:
        print("Exception in create_note", file=sys.stderr)
        return "Error: an unexpected error occurred while creating the note."


@mcp.tool()
async def get_note(
    secret_id: str,
    decryption_key: str,
    password: Optional[str] = None
) -> str:
    """
    Retrieve and decrypt a note from the securenote.link API.

    Args:
        secret_id:      The ID of the note to retrieve.
        decryption_key: The base64-encoded decryption key (from the URL fragment or create_note).
        password:       Required only if the note is password-protected.
    """
    # --- validate inputs ---
    if not secret_id or not secret_id.strip():
        return "Error: secret_id cannot be empty."
    if not decryption_key or not decryption_key.strip():
        return "Error: decryption_key cannot be empty."

    secret_id      = secret_id.strip()
    decryption_key = decryption_key.strip()

    if not _validate_secret_id(secret_id):
        return "Error: secret_id contains invalid characters."

    # Validate decryption_key is legitimate base64
    try:
        key_bytes = base64.b64decode(decryption_key, validate=True)
        if len(key_bytes) != 32:
            return "Error: decryption_key is not a valid 256-bit key."
    except Exception:
        return "Error: decryption_key is not valid base64."

    try:
        response = await make_api_request("GET", f"/api/v1/secrets/{secret_id}")
        if not response:
            return "Error: note not found. It may have expired, been read already, or never existed."

        content = response.get("content")

        # Password-protected notes require a verify call
        if response.get("passwordProtected"):
            if not password:
                return "This note is password-protected. Please provide the 'password' argument."
            verify = await make_api_request(
                "POST",
                f"/api/v1/secrets/{secret_id}/verify",
                {"password": password}
            )
            if not verify:
                return "Error: incorrect password or verification failed."
            content = verify.get("content")

        if not content:
            return "Error: no content in response. The note may require a password."

        encrypted_data = content.get("encryptedData")
        iv             = content.get("iv")
        if not encrypted_data or not iv:
            return "Error: response is missing encryptedData or iv."

        plaintext = decrypt_message_gcm(encrypted_data, decryption_key, iv)
        return plaintext

    except Exception:
        print("Exception in get_note", file=sys.stderr)
        return "Error: an unexpected error occurred while retrieving the note."


@mcp.tool()
async def get_instructions() -> str:
    """
    Returns a guide on how to use this secure note sharing service,
    intended for both humans and AI agents.
    """
    return f"""
## securenote.link MCP — Usage Guide

### Encryption Details
- **Algorithm**: AES-256-GCM
- **Key**: 256-bit, randomly generated per note, never stored on the server
- **IV**: 96-bit, randomly generated per note, stored alongside the ciphertext
- **Auth tag**: 128-bit, appended to the ciphertext

---

### Tools

#### `create_note(text, password=None, expires_in=24)`
Encrypts `text`, stores it on the server, and returns a JSON object with:
- `id` — the note's server-side identifier
- `key` — the base64 decryption key (never sent to the server)
- `url` — a one-click shareable link (`https://securenote.link?id=...#key`)
- `expires_in_hours` — when the note will be deleted
- `password_protected` — whether a password was set

**Limits**: text up to {MAX_TEXT_BYTES // 1000} KB · password up to {MAX_PASSWORD_BYTES} bytes

**One-click URL**: The decryption key is embedded in the URL fragment (`#`).
The fragment is never sent to the server, but it can appear in browser history.
For highly sensitive data, share the URL and key through separate channels.

**`expires_in` must be one of**: 1, 24, 72, or 168 hours.

---

#### `get_note(secret_id, decryption_key, password=None)`
Fetches the encrypted note from the server and decrypts it locally.
Returns the plain-text message on success.

> Note: most notes are **deleted from the server after first retrieval**.

---

### Security Recommendations
| Sensitivity | Approach |
|---|---|
| Low | Share the one-click `url` directly |
| High | Share `url` via one channel, `key` via a separate channel |
| Maximum | Add a `password` and share it via a third channel |
"""


if __name__ == "__main__":
    mcp.run(transport='stdio')
