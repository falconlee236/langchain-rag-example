from bs4 import BeautifulSoup
import aiohttp
import requests
from typing import Union
from langchain_community.document_loaders import RecursiveUrlLoader

def simple_metadata_extractor(
    raw_html: str, url: str, response: Union[requests.Response, aiohttp.ClientResponse]
) -> dict:
    content_type = getattr(response, "headers").get("Content-Type", "")
    return {"source": url, "content_type": content_type}

def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title = ""
    content = ""
    title_object = soup.find("h1", "devsite-page-title")
    if title_object is not None:
        title = "title: " + title_object.text.strip() + "\n\n"
    content_object = soup.find("div", "devsite-article-body clearfix")
    if content_object is not None:
        content = content_object.text.strip()
    return title + content


def get_docs() -> list[str]:    
    """    
	Docs
	Let's apply this to LangChain's LCEL documentation.

	In this case, each doc is a unique web page of the LCEL docs.

	The context varies from < 2k tokens on up to > 10k tokens.
    """
    # LCEL docs
    url = "https://cloud.google.com/docs/overview"
    loader = RecursiveUrlLoader(
		url=url, 
        max_depth=3, 
        extractor=bs4_extractor,
        metadata_extractor=simple_metadata_extractor,
	)
    docs = loader.load()
    
    docs_texts = [d.page_content for d in docs]
    print(len(docs))
    print(docs[0].page_content)
    print("---")
    print(docs[0].metadata)
    return docs_texts