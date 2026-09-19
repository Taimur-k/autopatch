# AutoPatch 🩹

**AutoPatch** is an AI-powered automated program repair system. Given a GitHub issue or bug report, AutoPatch analyzes the repository, localizes the fault, generates candidate patches using an AI/ML repair engine, validates those patches against the test suite, ranks the candidates, and optionally opens a GitHub pull request.

---

## Architecture

```
Frontend (React + Vite)
        ↓
Backend API (FastAPI)
        ↓
Repair Orchestrator
        ↓
┌─────────────────────────────────────────┐
│  Fault Localization (Ochiai, etc.)      │
│  Code Retrieval                         │
│  AI Repair Engine (LLM-based)           │
│  Patch Generation                       │
│  Patch Ranking                          │
│  Test Execution                         │
│  Git / GitHub Integration               │
└─────────────────────────────────────────┘
        ↓
  Repository / Benchmark
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Git

### 1. Clone & setup

```bash
git clone https://github.com/your-org/autopatch.git
cd autopatch
cp .env.example .env
# Edit .env with your tokens
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# UI available at http://localhost:5173
```

### 4. Docker (optional)

```bash
docker-compose up --build
```

---

## Project Structure

```
autopatch/
├── backend/          # FastAPI backend
├── frontend/         # React + TypeScript frontend
├── benchmark/        # Benchmark repositories and issues
├── docs/             # Architecture, workflow, research notes
├── scripts/          # Setup and utility scripts
├── .env.example      # Environment variable template
└── docker-compose.yml
```

## Documentation

- [Architecture](docs/architecture.md)
- [Workflow](docs/workflow.md)
- [Research](docs/research.md)
- [Development Guide](docs/development.md)

## License

MIT — see [LICENSE](LICENSE).

