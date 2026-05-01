from pydantic import BaseModel
from typing import List, Literal


EngagementLevel = Literal["LOW", "MEDIUM", "HIGH"]


class StudentResult(BaseModel):
    student_id: int
    attention_score: float
    engagement_score: float
    gd_score: float
    ml_engagement: EngagementLevel


class TrendData(BaseModel):
    frame: int
    attention: float
    engagement: float
    gd: float


class TopPerformer(BaseModel):
    student_id: int
    reason: str


class RankingItem(BaseModel):
    rank: int
    student_id: int
    score_summary: str


class IndividualReport(BaseModel):
    student_id: int
    attention: float
    engagement: float
    gd_score: float
    ml_insight: str
    strength: str
    weakness: str
    recommendation: str


class StructuredReport(BaseModel):
    top_performer: TopPerformer
    ranking: List[RankingItem]
    individual_reports: List[IndividualReport]
    final_summary: str


class AnalyzeResponse(BaseModel):
    students: List[StudentResult]
    trendData: List[TrendData]
    report: str
