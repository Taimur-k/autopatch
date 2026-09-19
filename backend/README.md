# AutoPatch – Backend

FastAPI backend for the AutoPatch automated program repair system.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
```

## Run

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Test

```bash
pytest tests/ -v
```

## Lint

```bash
ruff check app/
ruff format app/
```

## Structure

```
app/
├── main.py                  # FastAPI app factory
├── core/                    # Config, database session
├── models/                  # SQLAlchemy ORM models
├── api/                     # Route handlers
├── services/                # Business logic
├── agent/                   # Repair orchestrator & state
├── fault_localization/      # Fault localizer ABCs + Ochiai
├── repair/                  # Repair generator + ranker ABCs
├── retrieval/               # Code search + context builder
├── testing/                 # Test runner ABC + results
└── git/                     # Repo manager, diff, GitHub client
```

