# portfolio-cli

A terminal-style personal portfolio for Abhishek Dobliyal. The frontend is built with Vue 3 and Vite, and the backend provides live site stats plus a portfolio-scoped chat assistant backed by OpenRouter.

## Features

- Terminal-inspired portfolio UI
- Command-driven navigation with aliases and suggestions
- Animated particle background and CLI easter eggs
- Live GitHub, LeetCode, and Chess.com profile stats
- Site analytics persisted through a FastAPI + MongoDB backend
- Portfolio-only AI chat assistant with streamed responses
- Responsive layout for desktop and mobile

## Tech Stack

### Frontend

- Vue 3
- Vite
- Tailwind CSS
- Three.js

### Backend

- FastAPI
- MongoDB
- PyMongo
- HTTPX
- OpenRouter

## Project Structure

```text
.
|-- src/        # Vue frontend
|-- public/     # static assets
|-- backend/    # FastAPI backend
```

## Getting Started

### Prerequisites

- Node.js 18+
- npm
- Python 3.10+
- `uv` or `pip`
- MongoDB connection details
- OpenRouter API key

### Frontend Setup

```bash
npm install
npm run dev
```

### Backend Setup

From `backend/`:

```bash
uv venv
uv pip install -r requirements.txt
```

Create `backend/.env` from `backend/.env.example` and set:

- `MONGO_URI`

Or use the split Mongo settings:

- `MONGO_USERNAME`
- `MONGO_PASSWORD`
- `MONGO_HOST`
- `MONGO_OPTIONS`

Also set:

- `OPEN_ROUTER_KEY`

Then run the backend from `backend/`:

```bash
uv run uvicorn app:app --reload
```

## Available Commands

Core commands:

- `/about`
- `/skills`
- `/projects`
- `/timeline`
- `/stats`
- `/profiles`
- `/site`
- `/chat <question>`
- `/contact`
- `/links`
- `/resume`
- `/help`
- `/clear`

Notes:

- `/chat` is portfolio-scoped and is not intended to behave like a general chatbot
- `/chat` responses may be slower on free-tier models
- some commands also support shortcuts and aliases inside the app

## Production Build

Frontend:

```bash
npm run build
npm run preview
```

Backend:

Run with your preferred ASGI process manager in `backend/`, for example:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8000
```

## Deployment

### Frontend

Deploy the frontend to Netlify.

Recommended settings:

- Build command: `npm run build`
- Publish directory: `dist`

### Backend

Deploy the FastAPI backend separately.

Current backend behavior:

- `/chat` and `/update-stats` are locked to the deployed portfolio origin
- chat uses OpenRouter through the backend so the API key stays server-side
- MongoDB is used for portfolio stats persistence

## Notes

- `node_modules/`, `dist/`, and Python virtual environments are excluded from version control
- OpenRouter API keys expire yearly and should be rotated
- Local frontend calls to the deployed backend will be blocked by CORS unless the backend explicitly allows your local origin
