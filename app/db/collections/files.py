from pydantic import Field
from typing import TypedDict, Optional
from pymongo.asynchronous.collection import AsyncCollection
from ..db import database


class FileSchema(TypedDict):
    name: str = Field(..., description="Name of the file")
    status: str = Field(..., description="status of the field")
    result: Optional[str] = Field(..., description="The result from Ai")
    
    
COLLECTION_NAME = "files"   
files_collection: AsyncCollection = database[COLLECTION_NAME]