from config import settings
from log.logger import Logger
from pymongo.mongo_client import MongoClient
from pymongo import errors


class Database:
    def __init__(self, uri=None, database_name=None, collection_name=None):
        self.mongo_uri = uri if uri else settings.build_mongo_uri()
        self.database_name = database_name if database_name else settings.database_name
        self._logger = Logger(__name__).get_logger()
        self._client = self._db = None
        self.collection_name = collection_name if collection_name else settings.collection_name

        self._connect()

    def _is_connected(self):
        return self._db is not None

    def _get_collection_name(self, collection_name=None):
        return collection_name if collection_name else self.collection_name

    def _get_collection(self, collection_name=None):
        if not self._is_connected():
            self._logger.error("database connection is not available")
            return None

        return self._db[self._get_collection_name(collection_name)]

    def _connect(self):
        """Connect to MongoDB."""
        if not self.mongo_uri:
            self._logger.error("missing MongoDB configuration in environment")
            return

        try:
            self._client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self._client.admin.command('ping')
            self._db = self._client[self.database_name]
            self._logger.info(f"successfully connected to the {self.database_name} database")
        except errors.ConnectionFailure as e:
            self._logger.error(f"connection to MongoDB failed: {str(e)}")
            self._client = None
            self._db = None
        except Exception as e:
            self._logger.error(f"error occurred while connecting to the database: {str(e)}")
            self._client = None
            self._db = None

    def find_one(self, collection_name=None, **query):
        """Find documents in the collection based on a query."""
        collection = self._get_collection(collection_name)
        if collection is None:
            return None

        try:
            document = collection.find_one(**query)
            return document
        except Exception as e:
            self._logger.error(f"an error occurred while finding documents: {str(e)}")
            return None

    def insert_document(self, document, collection_name=None):
        """Insert a document into the collection."""
        collection = self._get_collection(collection_name)
        if collection is None:
            return None

        try:
            result = collection.insert_one(document)
            self._logger.info(f"inserted document with id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            self._logger.error(f"error occurred while inserting document: {str(e)}")
            return None

    def update_document(self, query, update, collection_name=None, multiple=False):
        """Update documents in the collection based on a query."""
        collection = self._get_collection(collection_name)
        if collection is None:
            return None

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
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._logger.info("connection to database closed")
        else:
            self._logger.warning("no connection to close")
