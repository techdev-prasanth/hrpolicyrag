import os
import boto3
from dotenv import load_dotenv
load_dotenv()


client = boto3.client(
    "s3",
    endpoint_url=os.getenv("CLOUDFLARE_S3_URL"),
    aws_access_key_id=os.getenv("CLOUDFLARE_ACCESS_KEY")    ,
    aws_secret_access_key=os.getenv("CLOUDFLARE_SECRET_KEY"),
    region_name="auto",
)

print(client)