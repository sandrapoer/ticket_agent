# Ticket Agent (in progress)
This project is supposed to act as a ticketing system. This first part consists of a ticket REST API with role-based permissions and automated tests using `pytest`. 

Later, the system will include an LLM agent and a database.

## Setup 
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API
```bash
uvicorn main:app --reload
```
and open the interactive docs --> http://127.0.0.1:8000/docs

## Roles 
Since every request needs an `x-api-key` header, this key decides the role:

| Role   | Read tickets | Create tickets | Update status |
|--------|:------------:|:--------------:|:-------------:|
| reader | yes          | no             | no            |
| agent  | yes          | yes            | yes           |

Currently, those are hardcoded keys for demonstration.

## Access
| Method | Path                  | Description              | Success |
|--------|-----------------------|--------------------------|---------|
| GET    | `/tickets`            | List all tickets         | 200     |
| GET    | `/tickets/{ticket_id}`| Get one ticket           | 200     |
| POST   | `/tickets`            | Create a ticket          | 201     |
| PATCH  | `/tickets/{ticket_id}`| Update a ticket's status | 200     |

Not all error codes are listed.

## Tests
To run the tests using `pytest` with the `-v` flag for a more detailed output:
```bash
pytest -v
```

## Resources 
- FasAPI: https://fastapi.tiangolo.com/
- Uvicorn: https://uvicorn.dev/
- pytest: https://docs.pytest.org/en/stable/index.html
- httpx: https://www.python-httpx.org/
