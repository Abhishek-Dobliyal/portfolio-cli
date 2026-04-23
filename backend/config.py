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
