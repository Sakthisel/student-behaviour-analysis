# 📊 Sample Outputs

## CSV Output

Example:

```csv
student_id,attention_score,engagement_score,gd_score,ml_engagement
0,2.42,1.90,4.33,LOW
1,2.04,1.74,3.78,LOW
2,2.15,1.73,3.88,LOW
```

## ML Prediction

- LOW → Low participation
- MEDIUM → Moderate engagement
- HIGH → Active participation

## LLM Report

Example:

The student shows low engagement based on the ML classification.
The attention score indicates moderate focus, and the GD score reflects average performance.

Recommendation:
Improve participation and maintain consistent attention during discussions.

## Output Files

CSV:
`outputs/csv/student_summary.csv`

Models:
`models/trained_models/`

YOLO:
`runs/trained_models/weights/best.pt`