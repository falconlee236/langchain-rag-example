import asyncio
import json
import dotenv
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_community.document_loaders.url_playwright import PlaywrightEvaluator
from google.cloud import secretmanager_v1
import google_crc32c
from langchain_google_cloud_sql_pg import PostgresEngine, PostgresVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document
import re
import warnings
from sqlalchemy.exc import ProgrammingError

dotenv.load_dotenv()

eval_text = '''() => {
            let titleText = "", contentText = "", anchorsList = []
            const titleObject = document.querySelector("h1.devsite-page-title");
            titleText = titleObject ? titleObject.textContent.trim() : '';
            
            const contentObject = document.querySelector("div.devsite-article-body.clearfix");
            contentText = contentObject ? contentObject.textContent.trim() : '';
            
            if (contentObject) {
                const anchorsObject = Array.from(contentObject.querySelectorAll('a[href]'));   
                anchorsList = anchorsList ? anchorsObject.map(a => a.href) : [];
            }
            const data = {
                title: titleText,
                content: contentText.replace(/\\n\\n/g, ''),
                urls: anchorsList,
            };
            return JSON.stringify(data);
        }'''

class TestEvaluator(PlaywrightEvaluator):
    def evaluate(self, page, browser, response) -> str:
        """
        Extracts specific <a> tags from the page.

        Args:
            page (Page): The Playwright page object.
            browser (Browser): The Playwright browser instance.
            response (Response): The response from page.goto().

        Returns:
            str: The extracted links as newline-separated text.
        """
        # Extract <a> tags with href
        links = page.evaluate(eval_text)
        return links
    async def evaluate_async(self, page, browser, response) -> str:
        """
        Asynchronously extracts specific <a> tags from the page.

        Args:
            page (AsyncPage): The Playwright page object.
            browser (AsyncBrowser): The Playwright browser instance.
            response (AsyncResponse): The response from page.goto().

        Returns:
            str: The extracted links as newline-separated text.
        """
        links = await page.evaluate(eval_text)
        return links
    
    
class RecursivePlaywrightURLLoader:
    def __init__(self, evaluator, max_depth=3):
        self.max_depth = max_depth
        self.evaluator = evaluator
    
    async def load_documents(self, url_list, current_depth=0):
        if current_depth > self.max_depth:
            return []

        loader = PlaywrightURLLoader(
            urls=url_list,
            evaluator=self.evaluator
        )
        
        documents = []
        async for doc in loader.alazy_load():
            json_object = json.loads(doc.page_content)

            # 링크 추출
            links = json_object.get("urls", [])
            
            # 링크에서 문서를 계속 로드하기 위해 재귀 호출
            documents.extend(await self.load_documents(links, current_depth + 1))
                
            doc = Document(
                page_content=re.sub(r"\s+", " ", json_object.get("content", "")),
                metadata={
                    **doc.metadata,
                    "title": json_object.get("title", ""),
                },
            )
            documents.append(doc)
        
        return documents

def access_secret_version(project_id: str, secret_id: str) -> str:
    # Create a Client
    client = secretmanager_v1.SecretManagerServiceClient()

    # Initialize request arguments
    request = secretmanager_v1.AccessSecretVersionRequest(
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    )

    # Access the secret version
    response = client.access_secret_version(
        request=request
    )

    # Verify payload checksum
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print("Data corruption detected.")
        return ""

    # payload = response.payload.data -> bytes
    payload = response.payload.data.decode("UTF-8")
    return payload

def get_docs() -> list[str]:    
    """    
	Docs
	Let's apply this to LangChain's LCEL documentation.

	In this case, each doc is a unique web page of the LCEL docs.

	The context varies from < 2k tokens on up to > 10k tokens.
    """
    # 사용할 URL과 로더 설정
    start_url = "https://cloud.google.com/docs/overview?hl=en"
    loader = RecursivePlaywrightURLLoader(TestEvaluator(), max_depth=0)

    # 문서 로딩 시작
    docs = asyncio.run(loader.load_documents([start_url]))
    
    return docs

def main():
    # https://python.langchain.com/docs/integrations/vectorstores/google_cloud_sql_pg/
    # get connection
    engine = PostgresEngine.from_instance(
        project_id="optimap-438115",
        region="asia-northeast3",
        instance="postgresql-primary",
        database="root",
        user="root",
        password=access_secret_version(project_id="optimap-438115", secret_id="pg_password")
    )
    

    # init table
    try:
        engine.init_vectorstore_table(
            table_name="vector_store",
            vector_size=768, # Vector size for VertexAI/GenAI model(textembedding-gecko@latest)
        )
    except ProgrammingError:
        warnings.warn("found duplicate table name", UserWarning)
    
    # create embedding class instance
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

    # init default postgresvector store
    store = PostgresVectorStore.create_sync(
        engine=engine,
        table_name="vector_store",
        embedding_service=embedding,
    )
    
    # split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = get_docs()
    splits = text_splitter.split_documents(docs)

    store.from_documents(
        documents=splits,
        engine=engine,
        table_name="vector_store",
        embedding=embedding,
    )


if __name__ == "__main__":
    main()
    
    # retriever = store.as_retriever()

    # prompt = hub.pull('rlm/rag-prompt')
    
    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-1.5-pro",
    #     temperature=0,
    # )
    
    # rag_chain = (
    #     dict( # post-processing
    #         context=retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
    #         question=RunnablePassthrough()
    #     ) | prompt | llm | StrOutputParser()
    # )
    
    # # Question
    # print(rag_chain.invoke("What is Google Cloud Platform?"))

import functions_framework

@functions_framework.cloud_event
def my_cloudevent_function(cloud_event):
    print(cloud_event.data)