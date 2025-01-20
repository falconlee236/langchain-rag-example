from bs4 import BeautifulSoup, SoupStrainer
import aiohttp
import requests
from typing import Union
import json
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_community.document_loaders.url_playwright import PlaywrightEvaluator

def simple_metadata_extractor(
    raw_html: str, url: str, response: Union[requests.Response, aiohttp.ClientResponse]
) -> dict:
    content_type = getattr(response, "headers").get("Content-Type", "")
    return {"source": url, "content_type": content_type}

def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title = ""
    content = ""
    title_object = soup.find("h1", {
        "class": "devsite-page-title"
    })
    if title_object is not None:
        title = "title: " + title_object.text.strip() + "\n\n"
    content_object = soup.find("div", {
        "class": "devsite-article-body clearfix"
    })
    if content_object is not None:
        content = content_object.text.strip()
        all_href_values = [tag['href'] for tag in content_object.find_all(href=True)]
    
    return title + content

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
    def __init__(self, evaluator, max_depth=3, ):
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
            # 문서 내용 출력
            print(f"Loaded Document from {"".join([str(x) + "\n" for x in url_list])} at depth {current_depth}")
            print(json.dumps(json.loads(doc.page_content), indent=4))

            # 링크 추출
            links = json.loads(doc.page_content).get("urls", [])
            
            # 링크에서 문서를 계속 로드하기 위해 재귀 호출
            documents.extend(await self.load_documents(links, current_depth + 1))
                
            
            documents.append(doc)
        
        return documents

def get_docs() -> list[str]:    
    """    
	Docs
	Let's apply this to LangChain's LCEL documentation.

	In this case, each doc is a unique web page of the LCEL docs.

	The context varies from < 2k tokens on up to > 10k tokens.
    """
    # LCEL docs
    # url = "https://cloud.google.com/docs/overview?hl=en"
    # loader = PlaywrightURLLoader(
    #     urls=[url],
    #     evaluator=TestEvaluator()
    # )
    # for doc in loader.lazy_load():
    #     print(doc.metadata)
    #     print(json.dumps(json.loads(doc.page_content), indent=4))
    # 사용할 URL과 로더 설정
    start_url = "https://cloud.google.com/docs/overview?hl=en"
    loader = RecursivePlaywrightURLLoader(TestEvaluator(), max_depth=2)

    # 문서 로딩 시작
    import asyncio
    docs = asyncio.run(loader.load_documents([start_url]))
    # docs = loader.load_documents([start_url])
    print(len(docs))
    return ["hello"]