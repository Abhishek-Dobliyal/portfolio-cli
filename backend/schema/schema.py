from datetime import datetime
from typing import Dict, List
from bson import ObjectId

from pydantic import BaseModel, Field


class MaxVisits(BaseModel):
    cnt: int = 0
    date: str

    
class VisitorStats(BaseModel):
    visitors_cnt: int
    tab_stats: Dict[str, int]
    max_visits: MaxVisits
    current_day_cnt: Dict[str, int]
    connect_attempt_cnt: int
    avg_session_seconds: float


class UpdateVisitorStats(BaseModel):
    visitors_cnt: int
    tab_stats: Dict[str, int]
    max_visits: MaxVisits
    current_day_cnt: Dict[str, int]
    connect_attempt_cnt: int
    avg_session_seconds: float


class GetResponseModel(BaseModel):
    status_code: int
    message: str
    data: VisitorStats = {}


class UpdateResponseModel(BaseModel):
    status_code: int
    message: str
    updated_document_count: int = 0