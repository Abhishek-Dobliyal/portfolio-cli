import time
from datetime import datetime
from urllib.parse import urlsplit

from bson import ObjectId

from config import CHAT_RATE_LIMIT_COUNT, CHAT_RATE_LIMIT_WINDOW_SECONDS, STATS_DOCUMENT_ID, settings
from database.database import Database
from llm.openrouter import (
    OpenRouterConfigurationError,
    OpenRouterError,
    build_error_event,
    stream_chat_completion,
)
from log.logger import Logger
from schema.schema import ChatRequest, GetResponseModel, UpdateVisitorStats, UpdateResponseModel

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse

router = APIRouter()
db = Database()
custom_logger = Logger(__name__).get_logger()
chat_request_log = {}


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
        # Older clients reported session duration in a doubled unit.
        return avg_session_sec / 2

    return avg_session_sec


def close_database():
    db.close()


def _get_client_ip(request: Request):
    forwarded_for = request.headers.get('x-forwarded-for')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()

    return request.client.host if request.client else 'unknown'


def _enforce_chat_rate_limit(request: Request):
    client_ip = _get_client_ip(request)
    now = time.time()
    cutoff = now - CHAT_RATE_LIMIT_WINDOW_SECONDS
    recent_requests = [
        timestamp
        for timestamp in chat_request_log.get(client_ip, [])
        if timestamp >= cutoff
    ]

    if len(recent_requests) >= CHAT_RATE_LIMIT_COUNT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Chat rate limit reached. Please try again later.',
        )

    recent_requests.append(now)
    chat_request_log[client_ip] = recent_requests


def _extract_origin(url):
    if not url:
        return None

    parsed_url = urlsplit(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return None

    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def _require_allowed_origin(request: Request):
    allowed_origin = settings.get_frontend_origin()
    request_origin = _extract_origin(request.headers.get('origin'))
    request_referer_origin = _extract_origin(request.headers.get('referer'))

    if request_origin == allowed_origin or request_referer_origin == allowed_origin:
        return

    custom_logger.warning(
        'blocked request from disallowed origin: '
        f'origin={request.headers.get("origin")!r} '
        f'referer={request.headers.get("referer")!r} '
        f'ip={_get_client_ip(request)}'
    )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Request origin is not allowed.',
    )


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
async def update_stats(request: Request, stats: UpdateVisitorStats):
    _require_allowed_origin(request)

    stats_dict = stats.dict()
    stats_dict["avg_session_seconds"] = _normalize_avg_session_seconds(stats_dict)

    try:
        stats_document_id = ObjectId(STATS_DOCUMENT_ID)
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
        message="successfully updated the document",
        updated_document_count=resp["modified_count"]
    )


@router.post('/chat')
async def chat(request: Request, payload: ChatRequest):
    _require_allowed_origin(request)
    _enforce_chat_rate_limit(request)

    async def event_stream():
        try:
            async for chunk in stream_chat_completion(payload.message, payload.history):
                yield chunk
        except OpenRouterConfigurationError as exc:
            custom_logger.error(str(exc))
            yield build_error_event('Chat is currently unavailable. Please try again later or use /contact.')
        except OpenRouterError as exc:
            custom_logger.error(str(exc))
            yield build_error_event('The model is currently unavailable. Please try again shortly.')
        except Exception as exc:
            custom_logger.error(f'unexpected chat error: {str(exc)}')
            yield build_error_event('Unexpected chat error. Please try again later.')

    return StreamingResponse(event_stream(), media_type='text/event-stream')
