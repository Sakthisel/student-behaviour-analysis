# Student Behaviour Analysis Frontend

This is the React frontend dashboard for the Student Behaviour Analysis project.

## Features

- Upload group discussion video
- Run analysis pipeline
- View pipeline status
- Display attention, engagement and GD scores
- Show student-wise results
- Visualize score trends
- Display LLM-generated report

## Tech Stack

- React
- Vite
- Tailwind CSS
- Recharts
- Axios
- Lucide Icons

## Setup

```bash
npm install
```

## Environment

Create .env:

`VITE_API_BASE_URL=http://localhost:8000`

## Run
`npm run dev`
Backend Expected API
POST /analyze

Request:

multipart/form-data
file=<video>

Response:

{
  "students": [
    {
      "student_id": 0,
      "attention_score": 2.42,
      "engagement_score": 1.90,
      "gd_score": 4.33,
      "ml_engagement": "LOW"
    }
  ],
  "trendData": [
    {
      "frame": 1,
      "attention": 2.1,
      "engagement": 1.6,
      "gd": 3.5
    }
  ],
  "report": "Generated LLM report..."
}

## Build
`npm run build`

## Run:

```bash
npm install
npm run dev
