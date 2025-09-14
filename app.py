from fastapi import FastAPI
from item_scraper import AO3Scraper
from user_scraper import AuthorScraper
from tag_scraper import TagScraper
# 创建实例
app = FastAPI(title = "", description = "")

# 装饰器表明一旦有人访问http://服务器地址：端口/serach时执行装饰器下的函数
@app.get("/search")
def search(query:str):
    scraper = AO3Scraper()
    return scraper.html_conn(query)

@app.get("/users")
def author():
    scraper = AuthorScraper()
    return scraper.work_list

@app.get("/tags")
def tag():
    scraper = TagScraper()
    return scraper.tag_result_list
