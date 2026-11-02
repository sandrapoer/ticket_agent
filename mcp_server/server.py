import httpx
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from typing import Literal

API_URL: str = "http://127.0.0.1:8000"
API_KEY: str = "agent"
HEADERS: dict[str, str] = {"x-api-key": API_KEY}

# MCP Server gets same status & prio values as  the API
# LLM picks a valid value
TicketStatus = Literal["open", "in_progress", "closed"]
Priority = Literal["high", "medium", "low"]

mcp = MCPServer("ticket-system")

@mcp.tool()
def list_tickets() -> list[dict[str, str | int]]:
	"""List all tickets in the ticket system with their id, title, status and
	priority. Use this to get an overview before decidign which ticket to work on."""
	return call_api("GET", "/tickets").json()

# include a docstring for the LLM
@mcp.tool()
def get_ticket(ticket_id: int) -> dict[str, str | int]:
	"""Get one ticket by its id, including title, status and priority.
	If the id is unknown, use list_tickets."""
	return call_api("GET", f"/tickets/{ticket_id}").json()

@mcp.tool()
def create_ticket(title: str, priority: Priority = "low") -> dict[str, str | int]:
	"""Create a new ticket. New tickets always start with status "open".
	Use a short and clear title. Use "high" only for urgent problems.
	Use "medium" for problems that require more time but are not urgent."""
	return call_api("POST", "/tickets", {"title": title, "priority": priority}).json()

@mcp.tool()
def update_status(ticket_id: int, status: TicketStatus) -> dict[str, str | int]:
	"""Get one ticket by its id and update the status. Use "in_progress" 
	when work on the ticket starts and "closed" when the problem is solved.
	If the id is unknown, use list_tickets."""
	return call_api("PATCH", f"/tickets/{ticket_id}", {"status": status}).json()


# helper function for error handling
def call_api(method: str, path: str, body: dict[str, str] | None = None) -> httpx.Response:
	try:
		r: httpx.Response = httpx.request(method, f"{API_URL}{path}", json=body, headers=HEADERS)
	except httpx.ConnectError:
		raise ToolError("Ticket system not reachable. Do not retry now. Tell the user to retry later.")

	if r.status_code == 403:
		raise ToolError("Permission denied. This agent is not allowed to do this. Do not retry. Tell the user.")
	if r.status_code == 404:
		raise ToolError(f"Path <{path}> not found. Use list_tickets to find valid ticket ids.")
	if r.status_code == 422:
		raise ToolError(f"Input rejected by ticket system: {r.text}. Fix and try again.")

	r.raise_for_status()
	return r
	
# run with :
# mcp dev mcp_server/server.py