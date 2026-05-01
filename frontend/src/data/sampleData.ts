import { type Student, type TrendData } from "../types";

export const sampleStudents: Student[] = [
  {
    student_id: 0,
    attention_score: 2.42,
    engagement_score: 1.9,
    gd_score: 4.33,
    ml_engagement: "HIGH",
  },
  {
    student_id: 1,
    attention_score: 2.04,
    engagement_score: 1.74,
    gd_score: 3.78,
    ml_engagement: "MEDIUM",
  },
  {
    student_id: 2,
    attention_score: 2.15,
    engagement_score: 1.73,
    gd_score: 3.88,
    ml_engagement: "LOW",
  },
  {
    student_id: 3,
    attention_score: 1.85,
    engagement_score: 1.5,
    gd_score: 3.4,
    ml_engagement: "MEDIUM",
  },
  {
    student_id: 4,
    attention_score: 1.4,
    engagement_score: 1.1,
    gd_score: 2.95,
    ml_engagement: "LOW",
  },
];

export const sampleTrend: TrendData[] = [
  { frame: 1, attention: 2.1, engagement: 1.6, gd: 3.5 },
  { frame: 2, attention: 2.3, engagement: 1.8, gd: 3.9 },
  { frame: 3, attention: 2.4, engagement: 1.9, gd: 4.2 },
  { frame: 4, attention: 2.2, engagement: 1.7, gd: 3.8 },
  { frame: 5, attention: 2.5, engagement: 2.0, gd: 4.4 },
];

export const sampleReport = `Okay, let's analyze this student performance data and generate the requested output.\n\n**TOP PERFORMER:**\n\n*   Student ID: 0\n    *   Reason: This student consistently demonstrates the highest GD score (1.84) across all metrics. Their strong attention and engagement scores, combined with a high GD score, indicate a very effective learning approach.\n\n**RANKING:**\n\n1.  Student ID: 0 - 1.84\n2.  Student ID: 1 - 0.15\n3.  Student ID: 2 - 0.15\n4.  Student ID: 3 - 0.2\n5.  Student ID: 4 - -2.0\n\n**INDIVIDUAL REPORTS:**\n\n*   Student ID: 0\n    *   Attention: 0.47\n    *   Engagement: 1.37\n    *   Performance (GD): 1.84\n    *   ML Insight: LOW - The low engagement score suggests a potential need to explore ways to increase student motivation and participation.\n    *   Strength: High - The student's strong GD score indicates a solid grasp of the material.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation: Implement strategies to boost student engagement, such as incorporating interactive activities or providing immediate feedback.\n\n*   Student ID: 1\n    *   Attention: -0.02\n    *   Engagement: 1.26\n    *   Performance (GD): 1.24\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Medium - The student shows some engagement, but the low attention score indicates a need for improvement.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation:  Implement strategies to improve focus, such as brief mindfulness exercises or structured learning activities.\n\n*   Student ID: 2\n    *   Attention: 0.15\n    *   Engagement: 1.09\n    *   Performance (GD): 1.24\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Medium - The student shows some engagement, but the low attention score indicates a need for improvement.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation: Implement strategies to improve focus, such as brief mindfulness exercises or structured learning activities.\n\n*   Student ID: 3\n    *   Attention: -0.2\n    *   Engagement: 0.56\n    *   Performance (GD): 0.36\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Low - The student shows some engagement, but the low attention score indicates a need for improvement.\n    *   Weakness: Low - The low attention score indicates a need to focus on active learning strategies.\n    *   Recommendation: Implement strategies to improve focus, such as brief mindfulness exercises or structured learning activities.\n\n*   Student ID: 4\n    *   Attention: -2.0\n    *   Engagement: 0.0\n    *   Performance (GD): -2.0\n    *   ML Insight: LOW - The low attention score suggests a need to address potential distractions or lack of focus.\n    *   Strength: Very Low - The student shows a significant lack of engagement.\n    *   Weakness: Very Low - The student shows a significant lack of engagement.\n    *   Recommendation:  Immediate intervention to address the lack of engagement.\n\n**FINAL SUMMARY:**\n\nThe student with the highest GD score (1.84) is Student ID 0.  This student demonstrates a strong grasp of the material and consistently achieves high performance.  However, their low attention score suggests a need to proactively address potential distractions and focus on active learning strategies.  Further investigation into the reasons behind the low attention is recommended.\n\n---\n\nLet me know if you'd like me to refine this analysis or generate a different output!`;
