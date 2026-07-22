from langchain.agents import create_agent
from langchain_community.document_loaders  import PyPDFLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings  import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
import os
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,AIMessage,SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from prompt import prompt
load = load_dotenv(override=True)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)




def base():
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

        vector_store = QdrantVectorStore.from_existing_collection(
                embedding=embeddings,
                url = os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY"),
                collection_name="company_docs",
                prefer_grpc=True
            )

        retriever = vector_store.as_retriever(
            search_kwargs={"k": 3}
        )


        agent = create_agent(model="groq:llama-3.3-70b-versatile")
        while True:
            user_input = input(str("Ask HR questioons: ")).strip()

            if user_input.lower() == "q":
                print("Bye")
                break

            if not user_input:
                print("Please enter a valid question.")
                continue

            try:
                final_rag_result = agent.invoke(user_input)
                print(final_rag_result)
            except Exception as e:
                print("Something went wrong",e)
    except Exception as e:
            print("Initializtion Failed",e)



if __name__ == "__main__":
    base()
    