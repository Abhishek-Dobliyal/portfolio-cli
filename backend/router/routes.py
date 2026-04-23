from datetime import datetime
from bson import ObjectId

from database.database import Database
from log.logger import Logger
from schema.schema import GetResponseModel, UpdateVisitorStats, UpdateResponseModel

from fastapi import APIRouter, status

router = APIRouter()
db = Database()
custom_logger = Logger(__name__).get_logger()

@router.get("/get-stats", response_model=GetResponseModel)
async def get_stats():
    stats = db.find_one() # Fetch the document from collection

    # Set current day visit count to 0 every new day
    curr_day_cnt = stats["current_day_cnt"]
    curr_utc_date = datetime.utcnow().strftime("%Y-%m-%d")
    if curr_utc_date not in curr_day_cnt:
        stats["current_day_cnt"] = {curr_utc_date: 0}
    
    if not stats:
        return GetResponseModel(status_code=status.HTTP_200_OK, 
                                message="successfully fetched the documents")

    return GetResponseModel(status_code=status.HTTP_200_OK, 
                            message="successfully fetched the documents",
                            data=stats)


@router.post("/update-stats", response_model=UpdateResponseModel)
async def update_stats(stats: UpdateVisitorStats):
    stats_dict = stats.dict()
    avg_session_sec = stats_dict["avg_session_seconds"]
    if avg_session_sec >= 100:
        avg_session_sec = avg_session_sec / 2

    stats_dict["avg_session_seconds"] = avg_session_sec
    resp = db.update_document({"_id": ObjectId("669c9fa56b71ca0b7cfd81a5")},
                              {"$set": stats_dict})
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

@router.on_event("shutdown")
def shutdown():
    db.close()
