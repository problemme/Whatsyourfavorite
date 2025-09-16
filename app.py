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
def author(url: str  = Query(..., description = "作者主页完整链接")):
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

if __name__ == "__main__":
    #c 此为异步服务器网关接口
    import uvicorn
    # app指上面创建的实例，host是主机代码，可以决定谁能访问我的网页，port是端口号、即别人访问时的代码
    uvicorn.run(app, host="", port = 8000)

# 配置跨域访问
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许哪些域名访问该网站API
    allow_credentials=True, # 登录API是否需要cookie
    allow_methods=["*"], # 允许哪些HTTP方法
    allow_headers=["*"], # 允许哪些请求头
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
            if msg_type == "search":
                result = ao3_scraper.html_conn(message["query"])
                # 等待后端返回数据到前端（并保证它成功）
                await websocket.send_json({"type": "search_result", "data": result})
            elif msg_type == "author":
                author_scraper.get_work_list(message["url"])
                await websocket.send_json({"type": "author_result", "data": scraper.work_list})

            elif msg_type == "tag":
                tag_scraper.get_tag_list(message["url"])
                await websocket.send_json({"type": "tag_result", "data": scraper.tag_search_result})

            elif msg_type == "text":
                text_scraper.get_text_list(message["url"])
                await websocket.send_json({"type": "text_result", "data": scraper.full_text_list})

            else:
                await websocket.send_json({"error": "未知的请求类型"})
    except Exception as e:
        print("WebSocket关闭:", e)
    finally:
        await websocket.close()
