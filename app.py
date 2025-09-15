from fastapi import FastAPI, Query
from item_scraper import AO3Scraper
from user_scraper import AuthorScraper
from tag_scraper import TagScraper
from text_scraper import TextScraper
# 创建实例
app = FastAPI()
# 装饰器表明一旦有人访问http://服务器地址：端口/serach时执行装饰器下的函数
@app.get("/search")
def search(query:str):
    scraper = AO3Scraper()
    return scraper.html_conn(query)

@app.get("/users")
def author(url: str):
    scraper = AuthorScraper()
    scraper.get_work_list(url)
    print(scraper.work_list)
    return True

# 仅供点击tag链接跳转
@app.get("/tags")
def tag(url: str):
    scraper = TagScraper()
    scraper.get_tag_list(url)
    return scraper.tag_search_result

@app.get("/works")
def text(url: str):
    scraper = TextScraper()
    scraper.get_text_list(url)
    return scraper.full_text_list
