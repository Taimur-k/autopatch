#!/usr/bin/env bash
# AutoPatch setup script
# Usage: bash scripts/setup.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "📁  Project root: $ROOT_DIR"

# ── Copy .env if not present ──────────────────────────────────────────────────
if [ ! -f "$ROOT_DIR/.env" ]; then
  echo "📋  Copying .env.example → .env"
  cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
  echo "⚠️   Edit $ROOT_DIR/.env and add your API tokens before running the app."
else
  echo "✅  .env already exists — skipping."
fi

# ── Backend virtualenv + dependencies ─────────────────────────────────────────
BACKEND_DIR="$ROOT_DIR/backend"
VENV_DIR="$BACKEND_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
  echo "🐍  Creating Python virtual environment…"
  python3 -m venv "$VENV_DIR"
fi

echo "📦  Installing backend dependencies…"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$BACKEND_DIR/requirements.txt"
echo "✅  Backend dependencies installed."

# ── Frontend dependencies ─────────────────────────────────────────────────────
FRONTEND_DIR="$ROOT_DIR/frontend"

echo "📦  Installing frontend dependencies…"
cd "$FRONTEND_DIR" && npm install --silent
echo "✅  Frontend dependencies installed."

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "🎉  Setup complete!"
echo ""
echo "To start the backend:"
echo "  cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "To start the frontend:"
echo "  cd frontend && npm run dev"

