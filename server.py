from fastmcp import FastMCP

# 1. Initialize the Server
# "dependencies" tells the MCP host what Python packages we need (if it manages the env)
mcp = FastMCP("My Secure Server")

# --- Mock Database ---
# In real life, this would be Postgres or Salesforce
user_db = {
    "venkat": {"role": "admin", "salary": 200000},
    "guest": {"role": "visitor", "salary": 0}
}


# --- Tool 1: A Safe Tool ---
@mcp.tool()
def check_status() -> str:
    """Checks if the database is online. Safe for anyone to use."""
    return "System is Online. Database connection active."


# --- Tool 2: A Dangerous Tool (The Pallas Target) ---
@mcp.tool()
def get_user_salary(username: str) -> str:
    """
    Retrieves the salary for a specific user.
    WARNING: This contains PII (Personally Identifiable Information).
    """
    user = user_db.get(username.lower())
    if not user:
        return "User not found."

    return f"The salary for {username} is ${user['salary']}"


# --- Tool 3: An Admin Tool ---
@mcp.tool()
def delete_user(username: str) -> str:
    """
    Deletes a user from the database.
    RESTRICTED: Should only be called by Admins.
    """
    if username.lower() in user_db:
        del user_db[username.lower()]
        return f"User {username} deleted."
    return "User not found."


if __name__ == "__main__":
    mcp.run()