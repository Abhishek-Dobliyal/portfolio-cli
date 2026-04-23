import os

from log.logger import Logger

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo import errors

load_dotenv()

MONGO_URI_TEMPLATE = os.getenv('MONGO_URI')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_OPTIONS = os.getenv('MONGO_OPTIONS')
MONGO_URI = MONGO_URI_TEMPLATE.format(
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
    host=MONGO_HOST,
    options=MONGO_OPTIONS
)
DATABASE_NAME = "portfolio-analytics"
COLLECTION_NAME = "analytics"


class Database:
    def __init__(self, uri=None, database_name=None, collection_name=None):
        self.mongo_uri = uri if uri else MONGO_URI
        self.database_name = database_name if database_name else DATABASE_NAME
        self._logger = Logger(__name__).get_logger()
        self._client = self._db = None
        self.collection_name = collection_name if collection_name else COLLECTION_NAME
        
        self._connect()

    def _connect(self):
        """ Connects to MongoDB  """
        try:            
            self._client = MongoClient(self.mongo_uri)
            self._db = self._client[self.database_name]
            self._logger.info(f"successfully connected to the {self.database_name} database")
        except errors.ConnectionFailure as e:
            self._logger.error(f"connection to MongoDB failed: {str(e)}")
        except Exception as e:
            self._logger.error(f"error occurred while connecting to the database: {str(e)}")

    def find_one(self, collection_name=None, **query):
        """ Finds documents in the collection based on a query. """
        try: 
            document = self._db[collection_name if collection_name else self.collection_name].find_one(**query)
            return document
        except Exception as e:
            self._logger.error(f"An error occurred while finding documents: {str(e)}")
            return []

    def insert_document(self, document, collection_name=None):
        """ Inserts a document into the collection. """
        try:
            result = self._db[collection_name if collection_name else self.collection_name].insert_one(document)
            self._logger.info(f"inserted document with id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            self._logger.error(f"error occurred while inserting document: {str(e)}")
            return None

    def update_document(self, query, update, 
                        collection_name=None, 
                        multiple=False):
        """ Updates documents in the collection based on a query. """
        collection = self._db[collection_name if collection_name else self.collection_name]
        try:
            if multiple:
                result = collection.update_many(query, update)
                self._logger.info(f"matched {result.matched_count} documents and modified {result.modified_count} documents.")
                return {"matched_count": result.matched_count, "modified_count": result.modified_count}

            result = collection.update_one(query, update)
            self._logger.info(f"matched {result.matched_count} documents and modified {result.modified_count} documents.")
            return {"matched_count": result.matched_count, "modified_count": result.modified_count}
        except Exception as e:
            self._logger.error(f"error occurred while updating documents: {str(e)}")
            return None

    def close(self):
        """ Closes the MongoDB connection."""
        if self._client:
            self._client.close()
            self._logger.info("connection to database closed")
        else:
            self._logger.warning("no connection to close")
