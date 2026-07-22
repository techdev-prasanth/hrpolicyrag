from fastapi import FastAPI ,File , UploadFile
from knowledgebase.cloudflare_client import client
from tasks import file_upload_async
import os
from dotenv import load_dotenv
load_dotenv(override=True)
app = FastAPI()

from botocore.exceptions import ClientError
@app.post("/uploads/")
async def file_upload(file: UploadFile = File(...)):
    try:
        print("filema,e",file.file)
        print("filema,e",file.filename)
        r2_file = client.upload_fileobj(
                Fileobj = file.file,
                Bucket = os.getenv("CLOUDFLARE_BUCKET_NAME"),
                Key=file.filename,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
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




