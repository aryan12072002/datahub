# DataHub - Data Aggregation & Notification Service

A Django-based backend system that aggregates data from multiple sources (API/CSV), stores it efficiently, triggers asynchronous updates using Celery, and exposes optimized, cached APIs. Built with Django REST Framework, Celery, Redis, and AI-assisted development tools.

---

## 📦 Project Structure

```
datahub/
├─ datahub/
│  ├─ __init__.py
│  ├─ settings.py        # Django settings (DB, Redis, Celery config)
│  ├─ urls.py            # Project-level URL routing
│  ├─ asgi.py / wsgi.py  # Server entry points
├─ aggregator/
│  ├─ __init__.py
│  ├─ models.py          # DataSource, Record models
│  ├─ serializers.py     # DRF serializers
│  ├─ views.py           # API endpoints logic
│  ├─ urls.py            # App-level API routes
│  ├─ tasks.py           # Celery async tasks
│  ├─ admin.py           # Admin interface config
│  ├─ apps.py            # App registration
├─ manage.py             # Django CLI
├─ requirements.txt      # Python dependencies
├─ .env                  # Environment variables
├─ README.md             # Project documentation
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
git clone <repo_url>
cd datahub
```

2. **Create & activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**  
Create `.env` file with:
```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Start Django server**
```bash
python manage.py runserver
```

7. **Start Redis server**  
```bash
redis-server
```

8. **Start Celery worker**
```bash
celery -A datahub worker -l info
```

9. **Start Celery beat (for periodic tasks)**
```bash
celery -A datahub beat -l info
```

---

## 🏗️ Models

**DataSource**
- `name` – Name of the source
- `endpoint_url` – API URL or CSV file path
- `active` – Boolean flag for active sources

**Record**
- `source` – ForeignKey to DataSource
- `key` – Record identifier
- `value` – Data content
- `last_updated` – Timestamp of last update

---

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/data_sources/` | POST | Register a new data source |
| `/api/stats/` | GET | Get total records, data sources, average update time |

**Example Response for `/api/stats/`:**
```json
{
    "total_sources": 5,
    "total_records": 1024,
    "average_update_time": "12ms"
}
```

---

## ⚡ Celery & Async Updates

- Configured with Redis as broker & backend.
- Periodic task runs **every 30 minutes** to fetch data for all active sources.
- Bulk operations (`bulk_create` / `bulk_update`) used for efficiency.
- Cache invalidation on `/api/stats/` after each update.

---

## 🧰 Caching & Performance

- Redis caching implemented for:
  - `/api/stats/` endpoint
  - Optional top 10 updated records
- DRF rate limiting/throttling applied
- Metrics & profiling via Django Debug Toolbar or Silk
- Load tested with `locust` or `ab` for 1000 requests.

---

## 📝 Optimization & AI-Assisted Development

- **Bulk DB operations** and **select_related/prefetch_related** to reduce queries.
- **Redis caching** to reduce repeated DB hits.
- **Celery async tasks** prevent blocking API calls.
- AI tools used:
  - **Cursor/MCP/Copilot** – refactoring, code completion, boilerplate generation
- README includes **performance metrics before/after caching**.

---

## 🐳 Optional Enhancements

- Docker Compose setup for Django + Redis + Celery
- Environment-based settings (dev/staging/prod)
- Unit tests for at least one API endpoint and one Celery task

---

## 📊 Performance Metrics (Example)

| Test | Before Caching | After Caching |
|------|----------------|---------------|
| `/api/stats/` avg response | 120ms | 25ms |
| DB queries per request | 15 | 2 |
| Cache hit rate | 0% | 95% |

---

## 📚 References

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryproject.org/)
- [Redis](https://redis.io/)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- AI Tools: Cursor, MCP, Copilot

---

## ✅ Author

**Aryan Tayade** – Backend Developer | Django & Celery Enthusiast

