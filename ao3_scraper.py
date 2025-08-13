import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

class AO3Scraper:
    def __init__(self, session_cookie: str):
        self.session_cookie = 'eyJfcmFpbHMiOnsibWVzc2FnZSI6ImV5SnpaWE56YVc5dVgybGtJam9pTXpFek5tWmxaakZrTm1GbU9ERTNabUV4TW1aaVpqZzRPVEJqTTJVeE56RWlMQ0ozWVhKa1pXNHVkWE5sY2k1MWMyVnlMbXRsZVNJNlcxc3lNelV6TmpneE0xMHNJaVF5WVNReE5DUkJaekYxUlRKTE1HbHpVVUUxZGxKTVEyMXhPRGRsSWwwc0luSmxkSFZ5Ymw5MGJ5STZJaTkxYzJWeWN5OVVhR1ZrYjNOcFlTSXNJbDlqYzNKbVgzUnZhMlZ1SWpvaWVuUk5iRGw2TlY5YWJESXpOWFI1YmtWcmExazRhM0EzYjBwalVteFJSV2xKTXpVeE5GQmhYMGxLY3lKOSIsImV4cCI6IjIwMjUtMDgtMjNUMDU6MzM6MzguMzgxWiIsInB1ciI6ImNvb2tpZS5fb3R3YXJjaGl2ZV9zZXNzaW9uIn19--2d22e0e5ce95447bc994873910afb3f652597617'
        self.base_url = "https://archiveofourown.org"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/116.0.0.0 Safari/537.36"
            )
        }
        self.cookies = {
            "_otwarchive_session": self.session_cookie
        }
#获取最大页数的值
    def get_all_pages(self,html):
        soup = BeautifulSoup(html, "html.parser")
        #找到索引
        pagination = soup.select_one("ol.pagination.actions.pagy")
        pages = []
        for li in pagination.find_all("a"):
            try:
                num = int(li.text)
                pages.append(num)
            except ValueError:
                continue
        self.max_num = max(pages) if pages else 1
        return self.max_num
#对目标cp进行搜索        
    def search(self, query: str):
        #quote对字符串进行URL编码，query是cp关键词
        encoded_query = quote(query)
        text_list = []
        #爬取所有页面的信息
        for page in range(1, self.max_num+1):
            search_url = (
            f"{self.base_url}/works?utf8=✓"
            f"&work_search[query]={encoded_query}&page={page}"
        )
            response = requests.get(search_url, headers=self.headers, cookies=self.cookies)
            #抛出异常值
            if response.status_code != 200:
                raise Exception(f"请求失败：HTTP {response.status_code}")
            text_list.append(response.text)
        return self._parse_search_results(text_list)
#解析爬取的结果
    def _parse_search_results(self, html_list: list[str]):#okay我们可以记住这个表达
        results = []
        for html in html_list:
            soup = BeautifulSoup(html, "html.parser")
        #获取所有作品的列表    
        work_items = soup.find_all("li", class_="work blurb group")#返回所有作品的列表
        #循环以获得作品的名称、作者、tag和时间
        for item in work_items:
            div_header = item.find("div", class_="header module")
            header_module = div_header.find("h4", class_="heading").find("a")
            name = header_module.get_text(strip=True)
            name_url = "https://archiveofourown.org" + header_module["href"]
            author = header_module[1].get_text(strip=True)
            author_url = "https://archiveofourown.org" + header_module[1]["href"]
            ul_tags = item.find("ul", class_="tags commas")#class_防止和类的定义混淆
            tags = {}
            for li in ul_tags.find_all("li"):
                a_tag = li.find("a",class_ = "tag")
                if a_tag:
                    tag_text = a_tag.get_text(strip=True)
                    tag_url = "https://archiveofourown.org" + a_tag["href"]
                    tags[tag_text] = tag_url#字典构造规则
