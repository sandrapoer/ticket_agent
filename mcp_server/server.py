import httpx
from mcp.server import MCPServer
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
	r: httpx.Response = httpx.get(f"{API_URL}/tickets", headers=HEADERS)
	r.raise_for_status()
	return r.json()

# include a docstring for the LLM
@mcp.tool()
def get_ticket(ticket_id: int) -> dict[str, str | int]:
	"""Get one ticket by its id, including title, status and priority.
	If the id is unknown, use list_tickets."""
	r: httpx.Response = httpx.get(f"{API_URL}/tickets/{ticket_id}", headers=HEADERS)
	r.raise_for_status()
	return r.json()

@mcp.tool()
def create_ticket(title: str, priority: Priority = "low") -> dict[str, str | int]:
	"""Create a new ticket. New tickets always start with status "open".
	Use a short and clear title. Use "high" only for urgent problems.
	Use "medium" for problems that require more time but are not urgent."""
	r: httpx.Response = httpx.post(f"{API_URL}/tickets", json={"title": title, "priority": priority}, headers=HEADERS)
	r.raise_for_status()
	return r.json()

@mcp.tool()
def update_status(ticket_id: int, status: TicketStatus) -> dict[str, str | int]:
	"""Get one ticket by its id and update the status. Use "in_progress" 
	when work on the ticket starts and "closed" when the problem is solved.
	If the id is unknown, use list_tickets."""
	r: httpx.Response = httpx.patch(f"{API_URL}/tickets/{ticket_id}", json={"status": status}, headers=HEADERS)
	r.raise_for_status()
	return r.json()

# run with :
# mcp dev mcp_server/server.py