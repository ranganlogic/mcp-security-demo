import sys
import json
import subprocess
import os

# 1. Define the Policy (The Pallas Logic)
BLOCKED_USERS = ["venkat"]  # These users cannot be deleted


def is_malicious(line):
    """
    Analyzes the raw JSON traffic to detect intent.
    Returns: (is_blocked, error_message_dict)
    """
    try:
        msg = json.loads(line)

        # We only care about Tool Calls
        if msg.get("method") == "tools/call":
            params = msg.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            # POLICY: "No one can delete the Admin (Venkat)"
            if tool_name == "delete_user" and args.get("username", "").lower() in BLOCKED_USERS:
                return True, {
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "error": {
                        "code": -32003,
                        "message": f"🛡️ PALLAS GATEWAY BLOCKED: Deletion of protected user '{args['username']}' is forbidden."
                    }
                }
    except Exception:
        pass  # If JSON parse fails, let the server handle it

    return False, None


# 2. Start the Real Server as a Sub-Process
# We pipe stdin so we can control it.
# We let stdout go straight to system stdout (pass-through response).
process = subprocess.Popen(
    [sys.executable, "server.py"],  # Runs: python server.py
    stdin=subprocess.PIPE,
    stdout=sys.stdout,  # Server output goes directly back to Client
    stderr=sys.stderr,
    text=True,
    bufsize=0  # Unbuffered (Real-time)
)

# 3. The Traffic Loop (The "Man-in-the-Middle")
if __name__ == "__main__":
    sys.stderr.write("--- Pallas Gateway Active ---\n")

    while True:
        # Read one line from the Client (Inspector/Claude)
        line = sys.stdin.readline()
        if not line: break  # Connection closed

        # Check Security
        blocked, error_response = is_malicious(line)

        if blocked:
            # Case A: Attack Detected!
            # Send error back to Client immediately. Do NOT forward to Server.
            sys.stderr.write(f"[GATEWAY] Blocked malicious request: {line[:50]}...\n")
            print(json.dumps(error_response))
            sys.stdout.flush()
        else:
            # Case B: Safe Traffic.
            # Forward the line to the Real Server.
            try:
                process.stdin.write(line)
                process.stdin.flush()
            except BrokenPipeError:
                break