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

`VITE_API_BASE_URL=http://localhost:8000/api`

## Run
`npm run dev`
Backend Expected API
POST /analyze

Request:

multipart/form-data
file=<video>

Response:
```json
{
    "students": [
        {
            "student_id": 0,
            "attention_score": 0.47,
            "engagement_score": 1.37,
            "gd_score": 1.84,
            "ml_engagement": "LOW"
        },
        {
            "student_id": 1,
            "attention_score": -0.02,
            "engagement_score": 1.26,
            "gd_score": 1.24,
            "ml_engagement": "LOW"
        },
        {
            "student_id": 2,
            "attention_score": 0.15,
            "engagement_score": 1.09,
            "gd_score": 1.24,
            "ml_engagement": "LOW"
        },
        {
            "student_id": 3,
            "attention_score": -0.2,
            "engagement_score": 0.56,
            "gd_score": 0.36,
            "ml_engagement": "LOW"
        },
        {
            "student_id": 4,
            "attention_score": -2.0,
            "engagement_score": 0.0,
            "gd_score": -2.0,
            "ml_engagement": "LOW"
        }
    ],
    "trendData": [
        {
            "frame": 1,
            "attention": 0.47,
            "engagement": 1.37,
            "gd": 1.84
        },
        {
            "frame": 2,
            "attention": -0.02,
            "engagement": 1.26,
            "gd": 1.24
        },
        {
            "frame": 3,
            "attention": 0.15,
            "engagement": 1.09,
            "gd": 1.24
        },
        {
            "frame": 4,
            "attention": -0.2,
            "engagement": 0.56,
            "gd": 0.36
        },
        {
            "frame": 5,
            "attention": -2.0,
            "engagement": 0.0,
            "gd": -2.0
        }
    ],
    "report": "Okay, let's analyze this student performance data and generate the requested output.\n\n**TOP PERFORMER:**\n\n*   Student ID: 0\n    *   Reason: This student consistently demonstrates the highest GD score (1.84) across all metrics. Their strong attention and engagement scores, combined with a high GD score, indicate a very effective learning approach.\n\n**RANKING:**\n\n1.  Student ID: 0 - 1.84\n2.  Student ID: 1 - 0.15\n3.  Student ID: 2 - 0.15\n4.  Student ID: 3 - 0.2\n5.  Student ID: 4 - -2.0\n\n**INDIVIDUAL REPORTS:**\n\n*   Student ID: 0\n    *   Attention: 0.47\n    *   Engagement: 1.37\n    *   Performance (GD): 1.84\n    *   ML Insight: LOW - The low engagement score suggests a potential need to explore ways to increase student motivation and participation.\n    *   Strength: High - The student's strong GD score indicates a solid grasp of the material.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation: Implement strategies to boost student engagement, such as incorporating interactive activities or providing immediate feedback.\n\n*   Student ID: 1\n    *   Attention: -0.02\n    *   Engagement: 1.26\n    *   Performance (GD): 1.24\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Medium - The student shows some engagement, but the low attention score indicates a need for improvement.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation:  Implement strategies to improve focus, such as brief mindfulness exercises or structured learning activities.\n\n*   Student ID: 2\n    *   Attention: 0.15\n    *   Engagement: 1.09\n    *   Performance (GD): 1.24\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Medium - The student shows some engagement, but the low attention score indicates a need for improvement.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation: Implement strategies to improve focus, such as brief mindfulness exercises or structured learning activities.\n\n*   Student ID: 3\n    *   Attention: -0.2\n    *   Engagement: 0.56\n    *   Performance (GD): 0.36\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Low - The student shows some engagement, but the low attention score indicates a need for improvement.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation: Implement strategies to improve focus, such as brief mindfulness exercises or structured learning activities.\n\n*   Student ID: 4\n    *   Attention: -2.0\n    *   Engagement: 0.0\n    *   Performance (GD): -2.0\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Very Low - The student shows a significant lack of engagement.\n    *   Weakness: Very Low - The student shows a significant lack of engagement.\n    *   Recommendation:  Immediate intervention to address the lack of engagement.\n\n**FINAL SUMMARY:**\n\nThe student with the highest GD score (1.84) is Student ID 0.  This student demonstrates a strong grasp of the material and consistently achieves high performance.  However, their low attention score suggests a need to proactively address potential distractions and focus on active learning strategies.  Further investigation into the reasons behind the low attention is recommended.\n\n---\n\nLet me know if you'd like me to refine this analysis or generate a different output!"
}
```

## Build
`npm run build`

## Run:

```bash
npm install
npm run dev
