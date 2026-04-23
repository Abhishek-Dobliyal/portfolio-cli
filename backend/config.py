import os
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus, urlsplit

from dotenv import load_dotenv

load_dotenv()

MONGO_URI_TEMPLATE = 'mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority&appName={options}'
DATABASE_NAME = 'portfolio-analytics'
COLLECTION_NAME = 'analytics'
STATS_DOCUMENT_ID = '669c9fa56b71ca0b7cfd81a5'
OPEN_ROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
APP_URL = 'https://abhishek-dobliyal-portfolio.netlify.app/'
APP_NAME = 'Portfolio CLI'
CHAT_RATE_LIMIT_COUNT = 15
CHAT_RATE_LIMIT_WINDOW_SECONDS = 3600
CHAT_MAX_HISTORY_MESSAGES = 8
OPEN_ROUTER_MODELS = (
    'google/gemma-4-26b-a4b-it:free',
    'openrouter/free',
    'google/gemma-3-27b-it:free',
    'meta-llama/llama-3.3-70b-instruct:free',
)


@dataclass(frozen=True)
class Settings:
    mongo_uri: Optional[str] = os.getenv('MONGO_URI')
    mongo_username: Optional[str] = os.getenv('MONGO_USERNAME')
    mongo_password: Optional[str] = os.getenv('MONGO_PASSWORD')
    mongo_host: Optional[str] = os.getenv('MONGO_HOST')
    mongo_options: Optional[str] = os.getenv('MONGO_OPTIONS')
    open_router_key: Optional[str] = os.getenv('OPEN_ROUTER_KEY')

    def get_open_router_models(self):
        return list(OPEN_ROUTER_MODELS)

    def get_frontend_origin(self):
        parsed_url = urlsplit(APP_URL)
        return f'{parsed_url.scheme}://{parsed_url.netloc}'

    def get_mongo_config_mode(self):
        if self.mongo_uri:
            if all(token in self.mongo_uri for token in ('{username}', '{password}', '{host}', '{options}')):
                return 'templated_mongo_uri'

            return 'direct_mongo_uri'

        return 'split_mongo_fields'

    def build_mongo_uri(self):
        if self.mongo_uri:
            if all(token in self.mongo_uri for token in ('{username}', '{password}', '{host}', '{options}')):
                required_parts = [
                    self.mongo_username,
                    self.mongo_password,
                    self.mongo_host,
                    self.mongo_options,
                ]
                if all(required_parts):
                    return self.mongo_uri.format(
                        username=quote_plus(self.mongo_username),
                        password=quote_plus(self.mongo_password),
                        host=self.mongo_host,
                        options=quote_plus(self.mongo_options),
                    )

            return self.mongo_uri

        required_parts = [
            self.mongo_username,
            self.mongo_password,
            self.mongo_host,
            self.mongo_options,
        ]
        if not all(required_parts):
            return None

        return MONGO_URI_TEMPLATE.format(
            username=quote_plus(self.mongo_username),
            password=quote_plus(self.mongo_password),
            host=self.mongo_host,
            options=quote_plus(self.mongo_options),
        )


settings = Settings()
