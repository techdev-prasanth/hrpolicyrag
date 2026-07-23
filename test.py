from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv


print(os.getenv("QDRANT_URL"))
print(os.getenv("QDRANT_API_KEY"))
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    prefer_grpc=False,
)

print(client.get_collections())