from celery_pipeline import app ,shared_task
from knowledgebase.cloudflare_client import client 
import os
from botocore.exceptions import ClientError

@app.task
def add(x, y):
    print("File add file called from task")
    return x + y

@app.task
def run():
    print("File run file called from task run")

    print("100"*100)



@shared_task
def file_upload_async(file):
    upload = False
    try:
        if file:
            r2_file = client.upload_fileobj(
                Fileobj = file.file,
                Bucket = os.getenv("CLOUDFLARE_BUCKET_NAME"),
                Key=file.filename,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
        upload = True
        print("File uploaded successfully")

    except ClientError as e:
        print("File upload error",e)
        return e

    
    return upload