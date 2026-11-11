# Job Application Tracker API

A REST API to track job applications and see simple analytics about a job search.
Built with FastAPI, PostgreSQL and SQLAlchemy.

## Features

- Create, read, update and delete job applications
- Filter by status, search by company name, newest first
- Analytics: counts by status, applications per month, response rate
- Input validation (only allowed statuses: applied, interview, offer, rejected)
- Automated tests with pytest, using a separate test database

## Tech stack

Python, FastAPI, SQLAlchemy, PostgreSQL, Pydantic, pytest

## Endpoints

| Method | Path | What it does |
|--------|------|--------------|
| POST | /applications | Create an application |
| GET | /applications | List applications (`?status=` and `?company=` filters) |
| GET | /applications/{id} | Get one application (404 if missing) |
| PATCH | /applications/{id} | Update some fields of an application |
| DELETE | /applications/{id} | Delete an application |
| GET | /analytics/status-counts | Number of applications per status |
| GET | /analytics/monthly | Number of applications per month |
| GET | /analytics/summary | Total, waiting, responded and response rate |

## How to run

1. Clone the repository and open the folder.
2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the packages:

```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database called `job_tracker`, and set `DATABASE_URL` in `database.py` to match your PostgreSQL user.
5. Create the table:

```bash
python3 models.py
```

6. Start the server:

```bash
uvicorn main:app --reload
```

7. Open http://127.0.0.1:8000/docs to try the API in the browser.

## How to run the tests

1. Create a second PostgreSQL database called `job_tracker_test`.
2. Set `TEST_DATABASE_URL` in `conftest.py` to match your PostgreSQL user.
3. Run:

```bash
pytest -v
```

Tests never touch the real database. Every test starts with empty tables.