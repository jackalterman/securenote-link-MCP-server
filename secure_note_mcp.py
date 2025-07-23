from typing import Any, Optional, Tuple
import httpx
import base64
import secrets
from fastmcp import FastMCP
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Initialize FastMCP server
mcp = FastMCP("securenote.link")

# Constants
API_BASE_URL = "https://securenote.link"  # Update this to your server URL
VALID_EXPIRY_HOURS = [1, 24, 72, 168]

# Helper functions
async def make_api_request(method: str, endpoint: str, data: Optional[dict] = None) -> Optional[dict[str, Any]]:
    """Make a request to the secure notes API with proper error handling."""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
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
            print(f"API request timed out for {url}")
            return None
        except httpx.HTTPStatusError as e:
            print(f"API request failed with status {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            print(f"API request failed: {e}")
            return None

def generate_gcm_key_and_iv() -> Tuple[str, str]:
    """Generate a random 256-bit key and 96-bit IV for AES-GCM, both base64-encoded."""
    key = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')  # 32 bytes = 256 bits
    iv = base64.b64encode(secrets.token_bytes(12)).decode('utf-8')   # 12 bytes = 96 bits
    return key, iv

def encrypt_message_gcm(message: str, key: str, iv: str) -> str:
    """Encrypt a message using AES-256-GCM. Returns base64-encoded ciphertext+tag."""
    if not message:
        raise ValueError("Message cannot be empty")
    key_bytes = base64.b64decode(key)
    iv_bytes = base64.b64decode(iv)
    if len(key_bytes) != 32:
        raise ValueError("Key must be 32 bytes (256 bits)")
    if len(iv_bytes) != 12:
        raise ValueError("IV must be 12 bytes (96 bits) for GCM")
    encryptor = Cipher(
        algorithms.AES(key_bytes),
        modes.GCM(iv_bytes),
        backend=default_backend()
    ).encryptor()
    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    # GCM tag is 16 bytes, append to ciphertext
    result = ciphertext + encryptor.tag
    return base64.b64encode(result).decode('utf-8')

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

def validate_inputs(message: str, expires_in: int) -> Optional[str]:
    """Validate common inputs for secret creation. Returns error message if invalid, None if valid."""
    if not message or not message.strip():
        return "❌ Error: Message cannot be empty."
    if expires_in not in VALID_EXPIRY_HOURS:
        return f"❌ Error: expires_in must be one of: {', '.join(map(str, VALID_EXPIRY_HOURS))} hours."
    return None

async def create_encrypted_secret(message: str, password: Optional[str], expires_in: int) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Create an encrypted secret and store it via API.
    
    Returns:
        Tuple of (secret_id, encryption_key, error_message)
        If successful: (secret_id, key, None)
        If failed: (None, None, error_message)
    """
    try:
        # Generate key and IV, encrypt message
        key, iv = generate_gcm_key_and_iv()
        encrypted_data = encrypt_message_gcm(message.strip(), key, iv)

        # Prepare API request data
        api_data = {
            "encryptedData": encrypted_data,
            "iv": iv,
            "expiresIn": expires_in
        }
        if password:
            api_data["password"] = password

        # Send to API
        response = await make_api_request("POST", "/api/v1/secrets", api_data)
        if not response:
            return None, None, "❌ Failed to send secret to API. Please check if the server is running."
        
        secret_id = response.get("id")
        if not secret_id:
            return None, None, "❌ Error: No secret ID returned from API."

        return secret_id, key, None
        
    except Exception as e:
        return None, None, f"❌ Error creating encrypted secret: {str(e)}"

def format_security_info(password: Optional[str], expires_in: int) -> str:
    """Format common security information for responses."""
    password_line = "🔐 **Password Protected**: Yes\n" if password else ""
    return f"{password_line}⏰ **Expires In**: {expires_in} hours"

# MCP Tools
@mcp.tool()
async def send_secure_note_return_api_url_and_key(message: str, password: Optional[str] = None, expires_in: int = 24) -> str:
    """
    Encrypt a message, store it via the API, and return the retrieval URL and decryption key separately.

    This function is for advanced workflows where you want to handle retrieval and decryption yourself.
    It returns:
      - The API URL to retrieve the encrypted message (returns JSON, not a user-facing page)
      - The decryption key (base64-encoded, to be used separately)

    After calling this function, you (or your code) must:
      - Use your own code to fetch the encrypted message from the API and decrypt it using the key,
        OR
      - Use the provided 'retrieve_and_decrypt_secret' method to fetch and decrypt the message via the API.

    Args:
        message: The secret message to encrypt and send.
        password: Optional password for additional protection.
        expires_in: Expiration time in hours (1, 24, 72, or 168).

    Returns:
        A formatted message containing:
          - The retrieval URL (API endpoint)
          - The decryption key (base64-encoded)
          - Security notes and usage instructions

    Security Note:
        For maximum security, share the URL and decryption key through different channels.
        If you want a single, user-friendly link, use 'send_secure_note' instead.

    ---
    Decryption process specifics:
    - The encryption algorithm used is AES-256-GCM.
    - The encrypted data is base64-encoded, with a separate IV (also base64-encoded).
    - The API's response structure is JSON with fields like 'encryptedData' and 'iv'.
    - The key is base64-encoded.

    Anyone writing their own decryption code must:
    - Correctly parse the API response (get 'encryptedData' and 'iv').
    - Base64-decode the key, iv, and encryptedData.
    - Use AES-256-GCM to decrypt, using the key and iv.
    """
    # Validate inputs
    error = validate_inputs(message, expires_in)
    if error:
        return error

    # Create encrypted secret
    secret_id, key, error = await create_encrypted_secret(message, password, expires_in)
    if error:
        return error

    api_retrieval_url = f"{API_BASE_URL}/api/v1/secrets/{secret_id}"
    security_info = format_security_info(password, expires_in)

    return f"""✅ Secret successfully encrypted and sent!

🔗 **API Retrieval URL** (returns JSON, not a user-facing page):
{api_retrieval_url}

🔑 **Decryption Key** (base64-encoded, keep this safe!):
{key}

{security_info}

⚠️ **Security Note**:
- The API URL above returns the encrypted data and IV in JSON format.
- The decryption key is NOT included in the URL and must be shared separately.
- For maximum security, share the URL and key through different channels.

📝 **How to Decrypt**:
- Use the 'retrieve_and_decrypt_secret' tool, or
- Write your own code to:
    1. Fetch the JSON from the API endpoint above
    2. Extract 'encryptedData' and 'iv' from the response
    3. Base64-decode the key, iv, and encryptedData
    4. Decrypt using AES-256-GCM with the key and iv

🔒 **Recommendation**:
If you want a single, user-friendly link, use 'send_secure_note' instead (less secure).
"""

@mcp.tool()
async def retrieve_and_decrypt_secret(secret_id: str, decryption_key: str, password: Optional[str] = None) -> str:
    """Retrieve and decrypt a secret from the API.
    
    Args:
        secret_id: The ID of the secret to retrieve
        decryption_key: The decryption key (base64 encoded)
        password: Optional password if the secret is password protected
    """
    try:
        # Validate inputs
        if not secret_id or not secret_id.strip():
            return "❌ Error: Secret ID cannot be empty."
        
        if not decryption_key or not decryption_key.strip():
            return "❌ Error: Decryption key cannot be empty."
        
        secret_id = secret_id.strip()
        decryption_key = decryption_key.strip()
        
        # First, retrieve the encrypted data from the API
        response = await make_api_request("GET", f"/api/v1/secrets/{secret_id}")
        
        if not response:
            return "❌ Failed to retrieve secret. It may have expired, been deleted, or never existed."
        
        # Check if password is required
        if response.get("passwordProtected") and not password:
            return "🔐 This secret is password protected. Please provide the password."
        
        # If password is required, verify it
        if password:
            verify_response = await make_api_request("POST", f"/api/v1/secrets/{secret_id}/verify", {"password": password})
            if not verify_response:
                return "❌ Incorrect password or verification failed."
            content = verify_response.get("content")
        else:
            content = response.get("content")
        
        if not content:
            return "❌ No encrypted content found in the response."
        
        encrypted_data = content.get("encryptedData")
        iv = content.get("iv")
        
        if not encrypted_data or not iv:
            return "❌ Missing encrypted data or IV in the response."
        
        decrypted_message = decrypt_message_gcm(encrypted_data, decryption_key, iv)
        
        return f"""✅ Secret successfully decrypted!

📝 **Message**:
{decrypted_message}

🔑 **Secret ID**: {secret_id}
"""
        
    except Exception as e:
        return f"❌ Error retrieving and decrypting secret: {str(e)}"

@mcp.tool()
async def check_api_health() -> str:
    """Check if the secure notes API is running and healthy."""
    try:
        response = await make_api_request("GET", "/api/v1/health")
        
        if response and response.get("status") == "ok":
            server_info = response.get("server", {})
            uptime = server_info.get("uptime", "unknown")
            version = server_info.get("version", "unknown")
            
            return f"""✅ API is healthy and running!

📊 **Server Info**:
- Status: OK
- Uptime: {uptime}
- Version: {version}
- URL: {API_BASE_URL}
"""
        else:
            return "❌ API is not responding correctly."
            
    except Exception as e:
        return f"❌ API health check failed: {str(e)}"

@mcp.tool()
async def send_secure_note(message: str, password: Optional[str] = None, expires_in: int = 24) -> str:
    """
    Encrypt a message, send it to the secure notes API, and generate a single, shareable URL (default app behavior).

    This function creates a user-friendly link that embeds both the secret ID and the decryption key.
    The recipient can simply click the link to view the message—no need to copy/paste keys separately.

    This is the default and recommended way to share secure notes in this app.

    Args:
        message: The secret message to encrypt and send
        password: Optional password for additional protection
        expires_in: Expiration time in hours (1, 24, 72, or 168)

    Returns:
        A formatted message containing the shareable URL and security notes.

    Security Note:
        The decryption key is included in the URL fragment (after '#'), which is not sent to the server,
        but may be visible in browser history or if the link is shared insecurely.
        For maximum security, consider sharing the key separately.
    """
    # Validate inputs
    error = validate_inputs(message, expires_in)
    if error:
        return error

    # Create encrypted secret
    secret_id, key, error = await create_encrypted_secret(message, password, expires_in)
    if error:
        return error

    # Create the one-click URL with embedded key
    secret_url_with_key = f"{API_BASE_URL}?id={secret_id}#{key}"
    security_info = format_security_info(password, expires_in)

    return f"""✅ Secret successfully encrypted and sent!

🔗 **One-Click Secret URL**:
{secret_url_with_key}

{security_info}

⚠️ **Security Warning**: 
This URL contains the decryption key in the fragment (after #). While convenient, this is less secure than sharing the key separately.

📝 **Usage**:
- Share this single URL with the recipient
- The key will be automatically extracted from the URL fragment
- The secret will still be encrypted on the server

🔒 **Recommendation**: 
For maximum security, use a password and share it through a separate channel.
"""

@mcp.tool()
async def get_instructions() -> str:
    """
    Provides a comprehensive guide on how to use this secure note sharing service, intended for both humans and AI agents.

    This guide explains the encryption process, the different methods for sharing secrets, and the tools available.

    """
    return """
    ###  Encryption Details

    - **Algorithm**: AES-256-GCM (Galois/Counter Mode)
      - **Key Size**: 256 bits (32 bytes)
      - **IV (Initialization Vector)**: 96 bits (12 bytes), randomly generated for each encryption.
      - **Authentication Tag**: 128 bits (16 bytes), appended to the ciphertext to ensure integrity and authenticity.

    - **Process**:
      1. A unique 256-bit encryption key and a 96-bit IV are generated for each new secret.
      2. The message is encrypted using AES-256-GCM.
      3. The encrypted data, along with the IV, is stored on the server.
      4. **Crucially, the encryption key is NEVER stored on the server.** It is the user's responsibility to manage the key.

    ---
    ### Available Tools & Sharing Workflows

    There are two primary workflows for sharing a secret:

    #### 1. Simple Sharing (One-Click URL)

    - **Tool**: `send_secure_note(message, password=None, expires_in=24)`
    - **How it works**:
      - Encrypts your message.
      - Stores the encrypted data on the server.
      - Generates a single URL that includes both the secret's ID and the decryption key in the URL fragment (`#`).
    - **Pros**:
      - **Convenient**: The recipient only needs to click one link.
    - **Cons**:
      - **Less Secure**: The key is part of the URL. While the fragment is not typically sent to the server, it can be exposed in browser history, logs, or if the link is shared insecurely.
    - **Use Case**: Best for low-sensitivity information where convenience is a priority.

    ---
    #### 2. Maximum Security Sharing (Two-Channel)

    This workflow requires two separate steps and is the recommended method for sensitive information.

    - **Step 1: Send the secret**
      - **Tool**: `send_secure_note_return_api_url_and_key(message, password=None, expires_in=24)`
      - **What it does**:
        - Encrypts your message.
        - Stores the encrypted data.
        - Returns the **API URL** and the **decryption key** as two separate pieces of information.

    - **Step 2: Retrieve the secret**
      - **Tool**: `retrieve_and_decrypt_secret(secret_id, decryption_key, password=None)`
      - **How it works**:
        - You must provide the `secret_id` (from the API URL) and the `decryption_key`.
        - The tool fetches the encrypted data from the server and decrypts it locally.
    - **Pros**:
      - **Most Secure**: The key is never transmitted with the URL. You should share the URL and the key through different channels (e.g., email the URL, text the key).
    - **Cons**:
      - Requires more steps for both the sender and the receiver.
    - **Use Case**: Best for highly sensitive data like passwords, API keys, or private information.

    ---
    ### Other Tools

    - **`check_api_health()`**:
      - Use this to verify that the secure note server is online and operational.
"""


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')