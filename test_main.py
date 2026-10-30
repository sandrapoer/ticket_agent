from fastapi.testclient import TestClient
from httpx import Response
from main import app

client: TestClient = TestClient(app)

AGENT: dict[str, str] = {"x-api-key": "agent"}
READER: dict[str, str] = {"x-api-key": "reader"}

def test_no_api_key() -> None:
	r: Response = client.get("/tickets")
	assert r.status_code == 401

def test_reader_reads() -> None:
	r: Response = client.get("/tickets", headers=READER)
	assert r.status_code == 200
	assert len(r.json()) >= 2

def test_reader_cannot_create() -> None:
	r: Response = client.post("/tickets", json={"title": "X"}, headers=READER)
	assert r.status_code == 403

def test_agent_can_create() -> None:
	r: Response = client.post("/tickets", json={"title": "X"}, headers=AGENT)
	assert r.status_code == 201
	assert r.json()["status"] == "open"

def test_agent_can_update() -> None:
	r: Response = client.patch("/tickets/1", json={"status": "closed"}, headers=AGENT)
	assert r.status_code == 200
	assert r.json()["status"] == "closed"

def test_reader_cannot_update() -> None:
	r: Response = client.patch("/tickets/1", json={"status": "closed"}, headers=READER)
	assert r.status_code == 403

def test_unknown_ticket() -> None:
	r: Response = client.get("/tickets/999", headers=READER)
	assert r.status_code == 404

# run tests with pytest