from typing import Dict, Optional

from pydantic import BaseModel


class MaxVisits(BaseModel):
    cnt: int = 0
    date: str


class VisitorStatsBase(BaseModel):
    visitors_cnt: int
    tab_stats: Dict[str, int]
    max_visits: MaxVisits
    current_day_cnt: Dict[str, int]
    connect_attempt_cnt: int
    avg_session_seconds: float


class VisitorStats(VisitorStatsBase):
    pass


class UpdateVisitorStats(VisitorStatsBase):
    pass


class GetResponseModel(BaseModel):
    status_code: int
    message: str
    data: Optional[VisitorStats] = None


class UpdateResponseModel(BaseModel):
    status_code: int
    message: str
    updated_document_count: int = 0
