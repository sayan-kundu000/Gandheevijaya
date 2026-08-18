# Gandheevijaya Database & Migration Architecture

## 1. Technology & Driver

- **ORM**: SQLAlchemy 2.x Declarative Base
- **PostgreSQL Driver**: `psycopg` (v3) via `postgresql+psycopg://`
- **Migration Tool**: Alembic

---

## 2. Connection Pooling Configuration

In production environments connecting to PostgreSQL:
```python
engine_kwargs = {
    "pool_size": 10,
    "max_overflow": 20,
    "pool_pre_ping": True,
    "pool_recycle": 1800,  # 30-minute connection recycling
}
```

---

## 3. Session Lifecycle Management

FastAPI routes obtain isolated database sessions using the `get_db()` dependency:

```python
@router.get("/items")
def list_items(db: Session = Depends(get_db)):
    ...
```

The generator guarantees:
1. Every request receives a clean session from the pool.
2. In the event of an unhandled exception, `db.rollback()` is invoked automatically.
3. The session is closed deterministically in the `finally:` block.

---

## 4. Alembic Migration Commands

To inspect the current database migration revision:
```bash
py -m alembic -c backend/alembic.ini current
```

To apply all pending migrations:
```bash
py -m alembic -c backend/alembic.ini upgrade head
```

To autogenerate a new migration after editing SQLAlchemy models:
```bash
py -m alembic -c backend/alembic.ini revision --autogenerate -m "describe_changes"
```
