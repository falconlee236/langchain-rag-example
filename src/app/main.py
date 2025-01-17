import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from preprocessor import get_docs
import dotenv

dotenv.load_dotenv()
    
all_texts = get_docs()

# Embed
vectorstore = Chroma.from_texts(
    texts=all_texts,
    embedding=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
)

# retriever
retriever = vectorstore.as_retriever(
    search_kwargs=dict(
        k=10, # 이러면 가장 가까운 10개만 가져옴 - default = 4
    )
)


#prompt
prompt = hub.pull("rlm/rag-prompt")
question = "What is task decomposition for LLM agents?"

# llm
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=300,
    api_key=os.environ["GROQ_API_KEY"],
)

rag_chain = (
    dict( # post-processing
        context=retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
        question=RunnablePassthrough()
    ) | prompt | llm | StrOutputParser()
)

# print(rag_chain.invoke(question))