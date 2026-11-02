import httpx
from mcp.server import MCPServer

API_URL: str = "http://127.0.0.1:8000"
API_KEY: str = "agent"
HEADERS: dict[str, str] = {"x-api-key": API_KEY}

mcp = MCPServer("ticket-system")

@mcp.tool()
def list_tickets() -> list[dict[str, str | int]]:
	r: httpx.Response = httpx.get(f"{API_URL}/tickets", headers=HEADERS)
	r.raise_for_status()
	return r.json()



# run with :
# mcp dev mcp_server/server.py