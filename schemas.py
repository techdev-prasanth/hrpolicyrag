from pydantic import BaseModel
from datetime import datetime

class PDFFileRequest(BaseModel):
    file_name: str | None = None
    file_type: str
    file_id: str


class PDFFileResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }