# AutoPatch – Frontend

React + TypeScript + Tailwind CSS frontend for AutoPatch.

## Setup

```bash
npm install
```

## Run (development)

```bash
npm run dev
# http://localhost:5173
# API requests are proxied to http://localhost:8000
```

## Build

```bash
npm run build
```

## Type-check

```bash
npm run typecheck
```

## Pages

| Route | Description |
|---|---|
| `/` | Dashboard — list of recent repair runs |
| `/new` | New Repair — form to submit a bug report |
| `/runs/:id` | Repair Run — full pipeline view with diff, fault locations, patches |

