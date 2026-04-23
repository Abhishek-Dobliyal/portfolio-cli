import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    mongo_uri_template: Optional[str] = os.getenv('MONGO_URI')
    mongo_username: Optional[str] = os.getenv('MONGO_USERNAME')
    mongo_password: Optional[str] = os.getenv('MONGO_PASSWORD')
    mongo_host: Optional[str] = os.getenv('MONGO_HOST')
    mongo_options: Optional[str] = os.getenv('MONGO_OPTIONS')
    database_name: str = os.getenv('DATABASE_NAME', 'portfolio-analytics')
    collection_name: str = os.getenv('COLLECTION_NAME', 'analytics')
    stats_document_id: str = os.getenv('STATS_DOCUMENT_ID', '669c9fa56b71ca0b7cfd81a5')
    allow_origin_regex: str = os.getenv('ALLOW_ORIGIN_REGEX', r'https://.*\.netlify\.app')
    open_router_key: Optional[str] = os.getenv('OPEN_ROUTER_KEY')
    open_router_url: str = os.getenv('OPEN_ROUTER_URL', 'https://openrouter.ai/api/v1/chat/completions')
    open_router_model: str = os.getenv('OPEN_ROUTER_MODEL', 'google/gemma-4-26b-a4b-it:free')
    open_router_fallback_models: str = os.getenv(
        'OPEN_ROUTER_FALLBACK_MODELS',
        'meta-llama/llama-3.3-70b-instruct:free,mistralai/mistral-small-3.2-24b-instruct:free',
    )
    app_url: str = os.getenv('APP_URL', 'https://portfolio-cli.netlify.app')
    app_name: str = os.getenv('APP_NAME', 'Portfolio CLI')
    chat_rate_limit_count: int = int(os.getenv('CHAT_RATE_LIMIT_COUNT', '15'))
    chat_rate_limit_window_seconds: int = int(os.getenv('CHAT_RATE_LIMIT_WINDOW_SECONDS', '3600'))
    chat_max_history_messages: int = int(os.getenv('CHAT_MAX_HISTORY_MESSAGES', '8'))

    def get_open_router_models(self):
        models = [self.open_router_model]
        fallback_models = [
            model.strip()
            for model in self.open_router_fallback_models.split(',')
            if model.strip()
        ]

        for model in fallback_models:
            if model not in models:
                models.append(model)

        return models

    def build_mongo_uri(self):
        required_parts = [
            self.mongo_uri_template,
            self.mongo_username,
            self.mongo_password,
            self.mongo_host,
            self.mongo_options,
        ]
        if not all(required_parts):
            return None

        return self.mongo_uri_template.format(
            username=self.mongo_username,
            password=self.mongo_password,
            host=self.mongo_host,
            options=self.mongo_options,
        )


settings = Settings()
