from fastapi import FastAPI, Query
from item_scraper import AO3Scraper
from user_scraper import AuthorScraper
from tag_scraper import TagScraper
from text_scraper import TextScraper
import json
from fastapi import WebSocket
# 创建实例
app = FastAPI()
# 装饰器表明一旦有人访问http://服务器地址：端口/serach时执行装饰器下的函数
@app.get("/search")
def search(query:str):
    scraper = AO3Scraper()
    return scraper.html_conn(query)

@app.get("/users")
def author(url: str = Query(..., description = "作者主页完整链接")):
    scraper = AuthorScraper()
    scraper.get_work_list(url)
    return scraper.work_list

# 仅供点击tag链接跳转
@app.get("/tags")
def tag(url: str = Query(...,description="作品tag完整链接")):
    scraper = TagScraper()
    scraper.get_tag_list(url)
    return scraper.tag_search_result

@app.get("/works")
def text(url: str = Query(..., description="作品正文完整链接")):
    scraper = TextScraper()
    scraper.get_text_list(url)
    return scraper.full_text_list
# 根路由，对开发者友好可以看到swagger文档
@app.get("/")
def root():
    return {"status": "ok", "msg": "Backend is running"}

# 配置跨域访问
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], # 允许哪些域名访问该网站API
    allow_credentials = False, # 登录API不需要cookie
    allow_methods = ["*"], # 允许哪些HTTP方法
    allow_headers = ["*"], # 允许哪些请求头
)
@app.websocket("/ws")
async def websocket_search(websocket: WebSocket):
    # 等待客户端消息，但由于是异步，其他的请求也能跑
    await websocket.accept()
    try:
        while True:
            # 加载由前端发来的消息
            data = await websocket.receive_text()
            ao3_scraper = AO3Scraper()
            author_scraper = AuthorScraper()
            tag_scraper = TagScraper()
            text_scraper = TextScraper()
            # 将前端消息json化
            message = json.loads(data)
            # 区分用户操作
            msg_type = message.get("type")
            # 用户在搜索框搜索
            if msg_type == "search":
                result = ao3_scraper.html_conn(message["query"])
                # 等待后端返回数据到前端（并保证它成功）
                await websocket.send_json({"type": "search_result", "data": result})
            # 用户点击作者链接 
            elif msg_type == "author":
                author_scraper.get_work_list(message["url"])
                await websocket.send_json({"type": "author_result", "data": author_scraper.work_list})
            # 用户点击tag链接
            elif msg_type == "tag":
                tag_scraper.get_tag_list(message["url"])
                await websocket.send_json({"type": "tag_result", "data": tag_scraper.tag_search_result})
            # 用户点击正文
            elif msg_type == "text":
                text_scraper.get_text_list(message["url"])
                await websocket.send_json({"type": "text_result", "data": text_scraper.full_text_list})
            else:
                await websocket.send_json({"type": "error", "message": "未知的请求类型"})
    except Exception as e:
        print("WebSocket关闭:", e)
    finally:
        await websocket.close()
