# Postpedia API

Postpedia API is a lightweight FastAPI backend that provides user registration, JWT authentication, full CRUD for posts, and an upvote/downvote voting system. It uses SQLAlchemy with PostgreSQL (managed via Alembic migrations) and Argon2 for secure password hashing. The API is suitable as the backend for a simple blog or social feed where authenticated users can create, edit, and vote on posts.

## Features
- User registration and JWT authentication
- Create / read / update / delete posts
- Upvote / downvote posts (vote counts included in post responses)
- PostgreSQL + SQLAlchemy with Alembic migrations
- Password hashing using Argon2 (`argon2-cffi`)
- OpenAPI docs available at `/docs` when running the app

## Project layout
- `app/` — application code
  - `app/main.py` — FastAPI app and router registration
  - `app/routers/post.py` — post endpoints
  - `app/routers/user.py` — user endpoints
  - `app/routers/auth.py` & `app/oauth2.py` — authentication and JWT helpers
  - `app/routers/vote.py` — voting endpoints
  - `app/models.py` — SQLAlchemy models
  - `app/schemas.py` — Pydantic schemas
  - `app/database.py` — DB engine and session
- `alembic/` — migration configuration and `versions/` with migration scripts
- `requirements.txt` — Python dependencies

## Requirements
- Python 3.10+ (or your project's target Python)
- PostgreSQL
- `argon2-cffi` for secure password hashing

Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment
Create a `.env` file in the project root with these values (used by `app/config.py`):

```
database_hostname=localhost
database_port=5432
database_name=your_db
database_username=your_user
database_password=your_password
secret_key=your_secret_key
algorithm=HS256
access_token_expire_minutes=30
```

## Setup
1. Create & activate a venv:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure your `.env`, create the database, then run migrations:
```bash
alembic upgrade head
```
4. Run the app:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Summary
- `POST /users` — register a new user (returns `UserOut`)
- `POST /login` or `POST /login/json` — login to receive JWT (`access_token`)
- `GET /posts` — list posts (includes vote counts)
- `POST /posts` — create a post (requires Authorization: Bearer token)
- `GET /posts/{id}` — get a single post with vote count
- `PUT /posts/{id}` — update a post (requires auth)
- `DELETE /posts/{id}` — delete a post (requires auth)
- `POST /vote` — add/remove a vote (requires auth)

Authentication: include the JWT in the `Authorization` header as `Bearer <access_token>` for protected endpoints.

## Notes
- Ensure the `.env` values are set and the DB user has the required privileges.
- Confirm `argon2-cffi` is installed for password hashing.
- Alembic migrations are present under `alembic/versions/`.

## License
Add a `LICENSE` file if you plan to publish this project.
