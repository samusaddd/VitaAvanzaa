
# VitaAvanza Backend (FastAPI)

## Quick start (local)

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env  # on Windows: copy .env.example .env
# edit .env and set JWT_SECRET_KEY, OPENAI_API_KEY, etc.

uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Docs: `http://127.0.0.1:8000/api/docs`

## Important endpoints

- `POST /api/auth/signup` – create user
- `POST /api/auth/login` – returns JWT (use as Bearer token from frontend)
- `GET /api/auth/me` – current user profile

- `POST /api/dvi/calculate` – store and return a DVI profile
- `GET /api/dvi/history` – list user's DVI profiles

- `GET /api/opportunities/` – list opportunities
- `POST /api/opportunities/` – create opportunity (for now, open – you can protect later)

- `GET /api/feed/` – list feed posts
- `POST /api/feed/` – create feed post (user needed)

- `POST /api/mitra/chat` – chat with Mitra (OpenAI-powered if API key set)

- `GET /health` – health check for Render
```