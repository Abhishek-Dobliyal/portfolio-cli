from datetime import datetime
from bson import ObjectId

from config import settings
from database.database import Database
from log.logger import Logger
from schema.schema import GetResponseModel, UpdateVisitorStats, UpdateResponseModel

from fastapi import APIRouter, status

router = APIRouter()
db = Database()
custom_logger = Logger(__name__).get_logger()


def _current_utc_date():
    return datetime.utcnow().strftime("%Y-%m-%d")


def _normalize_stats(stats):
    if not stats:
        return None

    current_day_count = dict(stats.get("current_day_cnt", {}))
    today = _current_utc_date()

    if today not in current_day_count:
        current_day_count[today] = 0

    normalized = dict(stats)
    normalized["current_day_cnt"] = current_day_count
    return normalized


def _normalize_avg_session_seconds(stats_dict):
    avg_session_sec = stats_dict.get("avg_session_seconds", 0)
    if avg_session_sec >= 100:
        return avg_session_sec / 2

    return avg_session_sec


def close_database():
    db.close()

@router.get("/get-stats", response_model=GetResponseModel)
async def get_stats():
    stats = _normalize_stats(db.find_one())

    if not stats:
        custom_logger.warning("stats document not found")
        return GetResponseModel(
            status_code=status.HTTP_200_OK,
            message="successfully fetched the documents",
        )

    return GetResponseModel(
        status_code=status.HTTP_200_OK,
        message="successfully fetched the documents",
        data=stats,
    )


@router.post("/update-stats", response_model=UpdateResponseModel)
async def update_stats(stats: UpdateVisitorStats):
    stats_dict = stats.dict()
    stats_dict["avg_session_seconds"] = _normalize_avg_session_seconds(stats_dict)

    try:
        stats_document_id = ObjectId(settings.stats_document_id)
    except Exception:
        custom_logger.error("invalid STATS_DOCUMENT_ID configuration")
        return UpdateResponseModel(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="invalid stats document configuration",
        )

    resp = db.update_document(
        {"_id": stats_document_id},
        {"$set": stats_dict},
    )

    if not resp:
        return UpdateResponseModel(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="could not update the document"
        )

    return UpdateResponseModel(
        status_code=status.HTTP_200_OK,
        message="successfully update the document",
        updated_document_count=resp["modified_count"]
    )
