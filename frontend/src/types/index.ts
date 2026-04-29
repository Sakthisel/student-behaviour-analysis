export type Status = "idle" | "processing" | "done";

export type EngagementLevel = "LOW" | "MEDIUM" | "HIGH";

export interface Student {
  student_id: number;
  attention_score: number;
  engagement_score: number;
  gd_score: number;
  ml_engagement: EngagementLevel;
}

export interface TrendData {
  frame: number;
  attention: number;
  engagement: number;
  gd: number;
}

export interface AnalyzeResponse {
  students?: Student[];
  trendData?: TrendData[];
  report?: string;
}
