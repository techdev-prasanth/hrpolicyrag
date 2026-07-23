from fastapi import FastAPI ,File , UploadFile , Depends
from knowledgebase.cloudflare_client import client
from tasks import file_upload_async
import os
from dotenv import load_dotenv
load_dotenv(override=True)
app = FastAPI()
from database import engine,session , Base, get_db
from schemas import PDFFileRequest,PDFFileResponse
from sqlalchemy.orm import Session
from models import PDFFile
import uuid

Base.metadata.create_all(bind=engine)



from botocore.exceptions import ClientError
@app.post("/uploads/")
async def file_upload(file: UploadFile = File(...),db: Session = Depends(get_db) ):
    try:
        print("filema,e",file.file)
        print("filema,e",file.filename)
        gen_uuid = uuid.uuid4()
        file_id = f"{file.filename}-{gen_uuid}"
        r2_file = client.upload_fileobj(
                Fileobj = file.file,
                Bucket = os.getenv("CLOUDFLARE_BUCKET_NAME"),
                Key=file.filename,
                ExtraArgs={
                    "ContentType": file.content_type,
                }
            )
        pdf_file = PDFFile(
        file_name=file.filename,
        file_id=file_id,
        file_type=file.content_type
    )

        db.add(pdf_file)
        db.commit()
        db.refresh(pdf_file)
        
        return ({
                "status_code":201,
                "status":"sucess",
                "message":"file has been uploaded, proccessing",
            })

    except ClientError  as e:
        print("Error",e)
        return ({
                "status_code": e.response["ResponseMetadata"]["HTTPStatusCode"],
                "status":"failed",
                "messages": e.response["Error"]["Message"]
            })




