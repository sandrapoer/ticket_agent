from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel


# create application instance that Uvicorn can serve
app = FastAPI()

# test database
tickets: dict[int, dict[str, str | int]] = {
	1: {"id": 1, "title": "PC broken", "status": "open", "priority": "low"},
	2: {"id": 2, "title": "WiFi not working", "status": "open", "priority": "high"}
}

# define user roles
API_KEYS: dict[str, str] = {"reader": "reader", "agent": "agent"}

# check permissions
def get_role(x_api_key: str | None) -> str:
	if x_api_key not in API_KEYS:
		raise HTTPException(status_code=401, detail="Invalid API key")
	return API_KEYS[x_api_key]

class NewTicket(BaseModel):
	title: str
	priority: str = "low"

# register GET endpoint at root URL
@app.get("/tickets")
def list_tickets(x_api_key: str | None = Header(None)) -> list[dict[str, str | int]]:
	get_role(x_api_key)
	return list(tickets.values())

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, x_api_key: str | None = Header(None)) -> dict[str, str | int]:
	get_role(x_api_key)
	if ticket_id not in tickets:
			raise HTTPException(status_code=404, detail="Ticket not found")
	return tickets[ticket_id]

@app.post("/tickets", status_code=201) 
def create_ticket(ticket: NewTicket, x_api_key: str | None = Header(None)) -> dict[str, str | int]:
	role = get_role(x_api_key)
	if role != "agent":
		raise HTTPException(status_code=403)
	new_id = max(tickets) + 1
	# turn new ticket into dict and unpack with **
	tickets[new_id] = {"id": new_id, "status": "open", **ticket.model_dump()}
	return tickets[new_id]

class StatusUpdate(BaseModel):
	status: str

@app.patch("/tickets/{ticket_id}")
def update_status(ticket_id: int, update: StatusUpdate, x_api_key: str | None = Header(None)) -> dict[str, str | int]:
	role: str = get_role(x_api_key)
	if role != "agent":
		raise HTTPException(status_code=403, detail="Not allowed to update ticket")
	if ticket_id not in tickets:
		raise HTTPException(status_code=404, detail="Ticket not found")
	tickets[ticket_id]["status"] = update.status
	return tickets[ticket_id]

# run with: 
# uvicorn main:app --reload