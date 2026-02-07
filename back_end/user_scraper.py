from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from back_end.item_scraper import AO3Scraper
import requests

ao3_scraper = AO3Scraper()
# 抓取时选择距离li标签最近的那个div
class AuthorScraper:
    def __init__(self):
        self.results = ao3_scraper.results
        self.work_list = {}

    def get_work_list(self, url):
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
            html = page.content()
        soup = BeautifulSoup(html, "lxml")
        work_items = soup.select("li.work.blurb.group")
        for item in work_items:
            div_header = item.find("div", class_="header module")
            header_module = div_header.find("h4", class_="heading")
            title = header_module.find("a", href = True)
            title_name = title.get_text(strip = True)
            title_url = "https://archiveofourown.org" + title["href"]
            self.work_list[title_name] = title_url
        return self.work_list

