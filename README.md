# TripLedger API

An AI-powered travel budget tracking REST API built with FastAPI, PostgreSQL, Redis, and Claude AI.

## What It Does

- Track travel expenses across multiple currencies with automatic conversion
- AI-powered expense categorization using Claude
- Natural language budget Q&A — ask "Am I on track?" and get an intelligent answer
- Group expense splitting with a graph-based debt simplification algorithm
- JWT authentication

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — relational database
- **Redis** — exchange rate caching
- **Claude API** — AI categorization and budget Q&A
- **Docker** — containerization
- **Terraform** — AWS ECS deployment
- **GitHub Actions** — CI/CD pipeline

## Local Setup

### Prerequisites
- Python 3.12+
- Docker Desktop

### Steps

1. Clone the repo
```bash
git clone https://github.com/SanjayRenukaprasad/tripledger.git
cd tripledger
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Fill in your values in .env
```

4. Start PostgreSQL and Redis
```bash
docker-compose up -d
```

5. Start the API
```bash
python3 -m uvicorn app.main:app --reload
```

6. Open API docs
```bash
http://127.0.0.1:8000/docs
```

## API Endpoints

### Auth
- `POST /auth/register` — register a new user
- `POST /auth/login` — login and get JWT token

### Trips
- `POST /trips` — create a trip
- `GET /trips` — list all your trips
- `GET /trips/{id}` — get a trip
- `PATCH /trips/{id}` — update a trip
- `DELETE /trips/{id}` — delete a trip

### Expenses
- `POST /trips/{id}/expenses` — add an expense (auto-categorized by Claude)
- `GET /trips/{id}/expenses` — list all expenses for a trip
- `DELETE /trips/{id}/expenses/{expense_id}` — delete an expense

### Members
- `POST /trips/{id}/members/{user_id}` — add a member to a trip
- `DELETE /trips/{id}/members/{user_id}` — remove a member

### AI
- `POST /trips/{id}/ask` — ask a natural language budget question
- `GET /trips/{id}/settle` — get minimum transactions to settle all debts

## Running Tests
```bash
python3 -m pytest tests/ -v
```

## Deployment

Infrastructure is defined in Terraform for AWS ECS deployment.
CI/CD is handled by GitHub Actions — tests run and deploy on every push to main.