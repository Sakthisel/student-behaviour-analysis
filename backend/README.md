# Student Behaviour Analysis Backend

FastAPI backend for the Student Behaviour Analysis project.

## Features

- Upload video
- Run analysis pipeline
- Return student-wise results
- Return trend chart data
- Return LLM-style report

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```uvicorn app.main:app --reload --port 8000```

## API

* Health Check
`GET /api/health`

* Analyze Video
`POST /api/analyze`

Request:
`multipart/form-data
file=<video>`

Response:
```json
{
  "students": [],
  "trendData": [],
  "report": ""
}
```

## Run Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend API should use: `VITE_API_BASE_URL=http://localhost:8000/api`
