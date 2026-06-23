# FastAPI Fresher Guide — Project + Interview Prep

---

## 🚀 Recommended Project: **Personal Task Manager API**

**Why this project?**

- Simple enough to build in 1–2 days
- Covers every concept he already knows (routes, DB, CRUD, SQLAlchemy, Pydantic, Dependency Injection)
- Easy to explain confidently in an interview
- Can be extended to show depth (auth, pagination, filtering)

---

## 📋 Project Overview

**"TaskFlow API"** — A RESTful backend for managing personal tasks with user authentication.

### Tech Stack

| Layer      | Tool                              |
| ---------- | --------------------------------- |
| Framework  | FastAPI                           |
| ORM        | SQLAlchemy                        |
| Validation | Pydantic v2                       |
| Database   | SQLite (dev) / PostgreSQL (prod)  |
| Auth       | JWT via `python-jose` + `passlib` |
| Server     | Uvicorn                           |

---

## 🗂️ Folder Structure

```
taskflow/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── users.py
│   └── tasks.py
├── dependencies.py
├── auth.py
└── requirements.txt
```

---

## 📌 Problem Statements (Build in Order)

### Problem 1 — Database Setup

**Goal:** Set up SQLAlchemy with SQLite and create two tables: `users` and `tasks`.

**Requirements:**

- `users` table: `id`, `username`, `email`, `hashed_password`, `created_at`
- `tasks` table: `id`, `title`, `description`, `status` (todo/in-progress/done), `priority` (low/medium/high), `user_id` (FK), `created_at`, `updated_at`
- Use `Base.metadata.create_all()` on startup

**Concepts covered:** SQLAlchemy models, relationships, Base, engine, SessionLocal

---

### Problem 2 — Pydantic Schemas

**Goal:** Create request/response schemas for Users and Tasks.

**Requirements:**

- `UserCreate` (username, email, password)
- `UserResponse` (id, username, email — no password!)
- `TaskCreate` (title, description, status, priority)
- `TaskUpdate` (all fields Optional)
- `TaskResponse` (all fields + created_at)
- Use `model_config = ConfigDict(from_attributes=True)` for ORM mode

**Concepts covered:** Pydantic models, field validation, schema separation, ORM mode

---

### Problem 3 — User Registration & Password Hashing

**Goal:** Build a `POST /users/register` endpoint.

**Requirements:**

- Accept `UserCreate` schema
- Hash password using `passlib` before saving
- Return `UserResponse` (never return raw password)
- Raise `HTTPException 400` if email already exists

**Concepts covered:** Password hashing, HTTPException, response_model

---

### Problem 4 — JWT Authentication

**Goal:** Build `POST /auth/login` that returns a JWT token.

**Requirements:**

- Accept `username` + `password` (OAuth2PasswordRequestForm)
- Verify password against hash
- Return `{"access_token": "...", "token_type": "bearer"}`
- Token should expire in 30 minutes

**Concepts covered:** OAuth2, JWT, token creation, `python-jose`

---

### Problem 5 — Dependency Injection for Auth

**Goal:** Create a `get_current_user` dependency.

**Requirements:**

- Use `OAuth2PasswordBearer` to extract token from header
- Decode JWT and fetch user from DB
- Raise `401 Unauthorized` if token is invalid/expired
- Inject this dependency into protected routes using `Depends()`

**Concepts covered:** Dependency Injection, `Depends()`, reusable auth logic

---

### Problem 6 — Full Task CRUD

**Goal:** Build all 5 CRUD endpoints for tasks (protected routes).

**Requirements:**

- `POST /tasks/` — Create task (auto-assign to logged-in user)
- `GET /tasks/` — List all tasks of logged-in user
- `GET /tasks/{task_id}` — Get single task (must belong to current user)
- `PUT /tasks/{task_id}` — Update task
- `DELETE /tasks/{task_id}` — Delete task
- Return `404` if task not found, `403` if task belongs to another user

**Concepts covered:** Full CRUD, path params, authorization logic, status codes

---

### Problem 7 (Bonus) — Query Filters & Pagination

**Goal:** Add filtering and pagination to `GET /tasks/`.

**Requirements:**

- Filter by `status` (`?status=todo`)
- Filter by `priority` (`?priority=high`)
- Add `skip` and `limit` query params for pagination
- Default: `skip=0`, `limit=10`

**Concepts covered:** Query parameters, SQLAlchemy `.filter()`, pagination

---

### Problem 8 (Bonus) — Background Task

**Goal:** Send a "welcome email" log when a user registers.

**Requirements:**

- Use FastAPI's `BackgroundTasks`
- After user creation, trigger a background task that logs: `"Welcome email sent to {email}"`
- The API response should NOT wait for this task

**Concepts covered:** BackgroundTasks, async behavior, non-blocking operations

---

## 🎯 Resume Bullet Points (Copy-paste ready)

```
• Built a RESTful Task Management API using FastAPI, SQLAlchemy ORM, and Pydantic v2
  with full CRUD operations, JWT-based authentication, and role-based access control.

• Implemented Dependency Injection for reusable authentication middleware,
  reducing code duplication across protected API endpoints.

• Designed normalized database schema with SQLAlchemy relationships,
  supporting user-task associations with cascading operations.

• Added query filtering and pagination to list endpoints,
  improving API performance for large datasets.
```

---

## 🎤 Interview Q&A Prep

### 🔵 Beginner Questions

**Q1: What is FastAPI and why use it over Flask?**

> FastAPI is a modern Python web framework built on Starlette and Pydantic. Key advantages: automatic OpenAPI docs generation, native async support, request/response validation via Pydantic, and it's significantly faster than Flask due to ASGI.

**Q2: What is Pydantic and why is it used in FastAPI?**

> Pydantic is a data validation library. In FastAPI, it's used to define request body schemas and response models. It automatically validates incoming data, coerces types, and raises clear validation errors. With `from_attributes=True`, it can serialize SQLAlchemy ORM objects directly.

**Q3: What is SQLAlchemy and what's the difference between the model and schema?**

> SQLAlchemy is a Python ORM. The **model** (SQLAlchemy) maps to a database table — it's what gets stored. The **schema** (Pydantic) defines what the API accepts or returns — it's for validation and serialization. They're kept separate because what you store and what you expose to clients are often different (e.g., never expose `hashed_password`).

**Q4: What is Dependency Injection in FastAPI?**

> It's a way to share reusable logic across routes using `Depends()`. For example, instead of writing auth logic in every route, you write it once as a dependency and inject it. FastAPI resolves dependencies automatically before calling the route function.

**Q5: What HTTP status codes did you use and why?**

> - `200 OK` — successful GET/PUT
> - `201 Created` — successful POST
> - `400 Bad Request` — validation error or duplicate data
> - `401 Unauthorized` — missing or invalid token
> - `403 Forbidden` — authenticated but not allowed (e.g., accessing another user's task)
> - `404 Not Found` — resource doesn't exist

---

### 🟡 Intermediate Questions

**Q6: How does JWT authentication work in your project?**

> On login, we verify the user's credentials and generate a JWT token using `python-jose`. The token contains the user's ID as a claim and has an expiry time. On subsequent requests, the client sends the token in the `Authorization: Bearer <token>` header. The `get_current_user` dependency decodes the token and fetches the user from DB for every protected route.

**Q7: What is the difference between `async def` and `def` in FastAPI routes?**

> `async def` is used when the route performs I/O-bound operations (like DB queries or external API calls) that benefit from async/await. `def` is for CPU-bound or sync operations. FastAPI runs `def` routes in a thread pool automatically. For most DB operations with SQLAlchemy (sync), `def` is fine.

**Q8: How does `response_model` work?**

> `response_model` tells FastAPI which Pydantic schema to use for the response. FastAPI will serialize the returned object using that schema and strip any fields not defined in it — this is how we prevent `hashed_password` from leaking even if we accidentally return the full ORM object.

**Q9: How did you handle the case where a user tries to update another user's task?**

> After fetching the task by `task_id`, I check if `task.user_id == current_user.id`. If not, I raise `HTTPException(status_code=403, detail="Not authorized")`. This is authorization logic, separate from authentication.

**Q10: What is `SessionLocal` and why do we use a generator dependency for it?**

> `SessionLocal` is a SQLAlchemy session factory. We use a generator dependency (`yield`) so the session is created before the request, passed to the route, and properly closed in the `finally` block after the request completes — even if an exception occurs. This prevents connection leaks.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 🔴 Advanced / Situational Questions

**Q11: How would you add rate limiting to your API?**

> I would use a middleware like `slowapi` (built on `limits` library) which integrates with FastAPI. You can add a `@limiter.limit("5/minute")` decorator per route or apply it globally via middleware.

**Q12: How would you move from SQLite to PostgreSQL?**

> Only the `DATABASE_URL` in `database.py` needs to change — from `sqlite:///./taskflow.db` to `postgresql://user:password@host/dbname`. SQLAlchemy abstracts the DB, so no model or query code changes. For production, we'd also use `psycopg2` as the driver.

**Q13: What is Alembic and why would you use it?**

> Alembic is a database migration tool for SQLAlchemy. Instead of using `create_all()` (which can't alter existing tables), Alembic generates versioned migration scripts. This lets you safely change your schema in production without losing data.

**Q14: How would you test your FastAPI application?**

> Using `pytest` and FastAPI's `TestClient`. You create a test DB, override the `get_db` dependency to use the test DB, and write tests for each endpoint. FastAPI's `TestClient` wraps `httpx` and lets you make requests without running a live server.

**Q15: What is the difference between `PUT` and `PATCH`?**

> `PUT` replaces the entire resource — all fields must be provided. `PATCH` does a partial update — only send the fields you want to change. In our project, we used `PUT` but made all `TaskUpdate` fields `Optional`, which technically behaves like `PATCH`.

---

## 📝 Quick Reference Cheat Sheet

```python
# Route with dependency injection
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return task
```

```python
# Pydantic schema with ORM mode
class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)
```

```python
# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

_Good luck to your brother! Build the project first, then read through the Q&A. The best interview answers come from actually having built the thing._
