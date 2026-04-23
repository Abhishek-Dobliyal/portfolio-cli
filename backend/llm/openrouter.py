import json

import httpx

from config import settings
from llm.context import SYSTEM_PROMPT


class OpenRouterError(Exception):
    pass


class OpenRouterConfigurationError(OpenRouterError):
    pass


class OpenRouterRateLimitError(OpenRouterError):
    pass


def ensure_openrouter_configured():
    if not settings.open_router_key:
        raise OpenRouterConfigurationError('OPEN_ROUTER_KEY is not configured')


def _trim_history(history):
    if not history:
        return []

    trimmed_history = history[-settings.chat_max_history_messages:]
    return [
        {'role': message.role, 'content': message.content}
        for message in trimmed_history
    ]


def build_messages(message, history):
    return [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        *_trim_history(history),
        {'role': 'user', 'content': message.strip()},
    ]


def build_error_event(message):
    payload = {'error': message}
    return f'data: {json.dumps(payload)}\n\ndata: [DONE]\n\n'


async def _stream_model_completion(client, headers, payload):
    async with client.stream('POST', settings.open_router_url, headers=headers, json=payload) as response:
        if response.status_code == 429:
            error_body = await response.aread()
            raise OpenRouterRateLimitError(
                f'OpenRouter request failed with status 429: {error_body.decode("utf-8", errors="ignore")}'
            )

        if response.status_code >= 400:
            error_body = await response.aread()
            raise OpenRouterError(
                f'OpenRouter request failed with status {response.status_code}: {error_body.decode("utf-8", errors="ignore")}'
            )

        async for chunk in response.aiter_text():
            if chunk:
                yield chunk


async def stream_chat_completion(message, history):
    ensure_openrouter_configured()

    headers = {
        'Authorization': f'Bearer {settings.open_router_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': settings.app_url,
        'X-Title': settings.app_name,
    }
    messages = build_messages(message, history)
    timeout = httpx.Timeout(connect=10.0, read=None, write=30.0, pool=10.0)
    models = settings.get_open_router_models()
    last_error = None

    async with httpx.AsyncClient(timeout=timeout) as client:
        for model in models:
            payload = {
                'model': model,
                'messages': messages,
                'stream': True,
            }

            try:
                async for chunk in _stream_model_completion(client, headers, payload):
                    yield chunk
                return
            except OpenRouterError as exc:
                last_error = exc
                continue

    if last_error:
        raise last_error

    raise OpenRouterError('OpenRouter request failed before a model response could be streamed')
