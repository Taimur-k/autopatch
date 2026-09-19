# AutoPatch – Development Guide

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.11+ |
| Node.js | 20+ |
| Git | any recent |
| Docker | optional |

---

## Quick Setup

```bash
# Clone the repo
git clone https://github.com/your-org/autopatch.git
cd autopatch

# Copy environment template
cp .env.example .env
# Edit .env — set GITHUB_TOKEN, OPENAI_API_KEY etc.

# Run the setup script (creates virtualenv + installs deps)
bash scripts/setup.sh
```

---

## Backend

### Install

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload
# http://localhost:8000
# http://localhost:8000/docs   ← Swagger UI
```

### Test

```bash
pytest tests/ -v
```

### Lint / Format

```bash
ruff check app/
ruff format app/
```

---

## Frontend

### Install

```bash
cd frontend
npm install
```

### Run

```bash
npm run dev
# http://localhost:5173
```

### Type-check

```bash
npm run typecheck
```

### Build for production

```bash
npm run build
```

---

## Docker

```bash
docker-compose up --build
# Backend:  http://localhost:8000
# Frontend: http://localhost:5173
```

---

## Environment Variables

See [`.env.example`](../.env.example) for all variables and their descriptions.

| Variable | Description |
|---|---|
| `DATABASE_URL` | SQLAlchemy async DB URL (default: SQLite) |
| `GITHUB_TOKEN` | GitHub PAT for PR creation |
| `OPENAI_API_KEY` | OpenAI API key for the repair engine |
| `CORS_ORIGINS` | Comma-separated list of allowed CORS origins |
| `DEBUG` | Enable SQLAlchemy query logging |

---

## Adding a New Fault Localiser

1. Create `backend/app/fault_localization/my_localizer.py`.
2. Subclass `FaultLocalizer` from `base.py`.
3. Implement `async def localize(self, repository, test_results) -> list[FaultLocation]`.
4. Inject it into `RepairOrchestrator.__init__()`.

## Adding a New Repair Generator

1. Create `backend/app/repair/my_generator.py`.
2. Subclass `RepairGenerator` from `base.py`.
3. Implement `async def generate(...)`.
4. Pass it to `RepairOrchestrator`.

---

## Project Conventions

- All async I/O uses `asyncio` / `async def` — no blocking calls in hot paths.
- Pydantic models for API schemas; SQLAlchemy models for persistence.
- ABCs define every pluggable component interface.
- `TODO:` comments mark where real implementations should go.
- Tests live in `backend/tests/`; use `pytest-asyncio` / `anyio`.

