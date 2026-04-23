from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


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


class ChatMessage(BaseModel):
    role: Literal['user', 'assistant']
    content: str = Field(..., min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: List[ChatMessage] = Field(default_factory=list)
