from langchain_community.document_loaders  import PyPDFLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore, RetrievalMode
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
load = load_dotenv(override=True)

FILE_PATH  = "D:\\ai_learning\\ai_projects\\hrpolicyrag\\HRPolicy.pdf"

def knowledge_ingest(args=None,**kwargs):
    loader = PyPDFLoader(FILE_PATH)

    try:
        documents  = loader.load()
        text_splitter  = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False

        )

        chunks = text_splitter.split_documents(documents)
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
        # embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004")
        vector = QdrantVectorStore.from_documents(
                chunks,
                embeddings,
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY"),
                collection_name="company_docs",
                retrieval_mode = RetrievalMode.DENSE,
                prefer_grpc=True
            )


        print("------------------")
        print("data successfully ingested",len(chunks))
    except Exception as e: 
        print("------------------")
        print(f"Ingestion Failed Due to {e}")




if __name__ ==  "__main__":
    knowledge_ingest()
