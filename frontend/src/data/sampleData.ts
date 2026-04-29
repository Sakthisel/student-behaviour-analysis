import { type Student, type TrendData } from "../types";

export const sampleStudents: Student[] = [
  {
    student_id: 0,
    attention_score: 2.42,
    engagement_score: 1.9,
    gd_score: 4.33,
    ml_engagement: "LOW",
  },
  {
    student_id: 1,
    attention_score: 2.04,
    engagement_score: 1.74,
    gd_score: 3.78,
    ml_engagement: "LOW",
  },
  {
    student_id: 2,
    attention_score: 2.15,
    engagement_score: 1.73,
    gd_score: 3.88,
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

export const sampleReport = `
The system detected low predicted engagement for most participants, while GD scores show moderate to strong discussion performance.

Students maintained reasonable attention, but visible participation can improve.

Recommendation: Encourage more active verbal and non-verbal participation while maintaining consistent attention during group discussion sessions.
`;
