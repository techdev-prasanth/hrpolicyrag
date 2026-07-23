from langchain_community.document_loaders  import PyMuPDFLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore, RetrievalMode 
from qdrant_client import QdrantClient
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
load = load_dotenv(override=True)
from knowledgebase.cloudflare_client import client 
import tempfile
from qdrant_client import models
import tempfile
from langchain_huggingface import HuggingFaceEmbeddings




embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

print()
print("embeddings",embeddings)
print()

print(os.getenv("QDRANT_URL"))
print(os.getenv("QDRANT_API_KEY"))

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None),
    timeout=120,
)

print()
print(qdrant_client.get_collections())
print()
COLLECTION_NAME = "enterprise_knowledgebase_v3"

print("QDRANT_URL:", os.getenv("QDRANT_URL"))
print("QDRANT_API_KEY:", os.getenv("QDRANT_API_KEY"))
print("COLLECTION_NAME:", COLLECTION_NAME)
print("LUSTER ID:", os.getenv("QDRANT_CLUSTER_ID"))



if not qdrant_client.collection_exists(COLLECTION_NAME):
    print()
    print("Enters in creating collection")
    print()
    try:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=384, 
                distance=models.Distance.COSINE
            ),
            
            )
    except Exception as e:
        print(f"Qdrant collection error : {e}")
else:
    print("collectio is already exist")

qdrant_vector = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,                 # Dense (Semantic)
    retrieval_mode=RetrievalMode.DENSE,
)
def ingest_doc():
    bucket  = os.getenv("CLOUDFLARE_BUCKET_NAME")
    print("Bucket :",bucket)
    response = client.list_objects_v2(Bucket=bucket)
    print("response :",response)

    for obj in response.get("Contents",[]):
        print(obj["Key"])
        key=obj["Key"]

    
        response = client.get_object(
                    Bucket=os.getenv("CLOUDFLARE_BUCKET_NAME"),
                    Key=key
                )
        
        print("Respnoe",response)
        pdf_bytes = response["Body"].read()

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf",delete=False) as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_path = tmp_file.name
                loader = PyMuPDFLoader(tmp_path)
                docs = loader.load()

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=200
                )
                print("docs :",len(docs))

                chunks = text_splitter.split_documents(docs)
                print("chunks",len(chunks))

                BATCH_SIZE = 20
                for i in range(0,len(chunks),BATCH_SIZE):
                    batch = chunks[i:i+BATCH_SIZE]
                    qdrant_vector.add_documents(batch)
                print("succesully injected")
        except Exception as e:
            print(f"Error processing {key}: {e}")

        finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)


if __name__ == "__main__":
    ingest_doc()