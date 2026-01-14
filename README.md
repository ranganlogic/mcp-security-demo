# MCP Security Demo: The "Man-in-the-Middle"

This project demonstrates the security vulnerabilities of the **Model Context Protocol (MCP)** and how to mitigate them using an interception gateway.

## Components

### 1. `server.py` (The Vulnerable Agent)
* A standard MCP server exposing a mock database.
* **Vulnerability:** It blindly executes tools like `delete_user` without checking permissions.

### 2. `gateway.py` (The Security Layer)
* A Python script that acts as a proxy between the Client (Claude/Inspector) and the Server.
* **Function:** Intercepts JSON-RPC traffic, inspects the `delete_user` tool call, and enforces a policy to block requests targeting Admins.

## How to Run

1. **Install Dependencies:**
   ```bash
   pip install "fastmcp[cli]"
 
## Run the Gateway (Security Enabled):

## Test the Attack:

### Try calling delete_user with argument venkat.

Result: BLOCKED by the gateway.
npx @modelcontextprotocol/inspector python gateway.py

