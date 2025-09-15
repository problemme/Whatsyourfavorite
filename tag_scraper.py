from item_scraper import AO3Scraper
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

ao3_scraper = AO3Scraper()
class TagScraper():
    def __init__(self):
        self.base_url = "https://archiveofourown.org"
        self.tag_search_result = []
        return True
    def get_tag_list(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)#加载谷歌浏览器
            context = browser.new_context()#类似于点击新建标签页
            context.add_cookies([{
                "name": "_otwarchive_session",   # AO3 的 cookie 名
                "value": "eyJfcmFpbHMiOnsibWVzc2FnZSI6ImV5SnpaWE56YVc5dVgybGtJam9pTXpFek5tWmxaakZrTm1GbU9ERTNabUV4TW1aaVpqZzRPVEJqTTJVeE56RWlMQ0ozWVhKa1pXNHVkWE5sY2k1MWMyVnlMbXRsZVNJNlcxc3lNelV6TmpneE0xMHNJaVF5WVNReE5DUkJaekYxUlRKTE1HbHpVVUUxZGxKTVEyMXhPRGRsSWwwc0luSmxkSFZ5Ymw5MGJ5STZJaTkxYzJWeWN5OVVhR1ZrYjNOcFlTSXNJbDlqYzNKbVgzUnZhMlZ1SWpvaWVuUk5iRGw2TlY5YWJESXpOWFI1YmtWcmExazRhM0EzYjBwalVteFJSV2xKTXpVeE5GQmhYMGxLY3lKOSIsImV4cCI6IjIwMjUtMDgtMjNUMDU6MzM6MzguMzgxWiIsInB1ciI6ImNvb2tpZS5fb3R3YXJjaGl2ZV9zZXNzaW9uIn19--2d22e0e5ce95447bc994873910afb3f652597617", 
                "domain": "archiveofourown.org",#写搜索网站的裸域名
                "path": "/"
            }])
            page = context.new_page()#打开了一页新的谷歌浏览页
            page.goto(url,wait_until = "domcontentloaded",timeout=150000)#跳转到搜索后的页面
            html = page.content()#获取对应网页渲染后的HTML
            soup = BeautifulSoup(html, "lxml")
    # 获取该页码所有作品的列表    
        work_items = soup.select("li.work.blurb.group")
    # 循环以获得作品的名称、作者、tag和时间
        for item in work_items:
            div_header = item.find("div", class_="header module")
            header_module = div_header.find("h4", class_="heading")
            #获取标题
            links = header_module.find_all("a")
            title_tag = links[0]
            name = title_tag.get_text(strip=True)
            name_url = self.base_url + title_tag["href"]
            #获取作者
            author_tag = links[1] if len(links) > 1 else None
            author = author_tag.get_text(strip=True) if author_tag else "Anonymous"
            author_url = self.base_url + author_tag["href"] if author_tag else None
            tags = []
            ul_tags = item.find("ul", class_="tags commas")#class_防止和类的定义混淆
            for li in ul_tags.find_all("li"):
                a_tag = li.find("a",class_ = "tag")
                if a_tag:
                    tag_text = a_tag.get_text(strip=True)
                    tag_url = self.base_url + a_tag["href"]
                    tag_piece = {"text": tag_text, "url": tag_url}
                    tags.append(tag_piece)
            work_info = {
                "title":{"text":name,"url":name_url},
                "author":{"text":author,"url":author_url},
                "tags":tags
            }
            self.tag_search_result.append(work_info)
        return self.tag_search_result
    
if __name__ =="main":

    tag_scraper = TagScraper()
    tag_scraper.get_tag_list(url = "")
