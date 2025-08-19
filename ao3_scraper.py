import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

class AO3Scraper:
    def __init__(self):
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
        pagination = soup.select_one("ol.pagination.actions")
        pages = []
        for li in pagination.find_all("a"):
            text = li.get_text(strip=True)
            try:
                pages.append(int(text))
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
            self.search_url = (
            f"{self.base_url}/works/search?page={page}"
            f"&work_search%5Bquery%5D={encoded_query}"
        )
            response = requests.get(self.search_url, headers=self.headers, cookies=self.cookies)
            #抛出异常值
            if response.status_code != 200:
                raise Exception(f"请求失败：HTTP {response.status_code}")
            text_list.append(response.text)
        return self._parse_search_results(text_list)
    
#解析爬取的结果
    def _parse_search_results(self, html_list: list[str]):#okay我们可以记住这个表达
        results = []
        #外循环所有页码
        for html in html_list:
            soup = BeautifulSoup(html, "html.parser")
        #获取该页码所有作品的列表    
            work_items = soup.find_all("li", class_="work blurb group")#返回所有作品的列表
        #循环以获得作品的名称、作者、tag和时间
            for item in work_items:
                div_header = item.find("div", class_="header module")
                header_module = div_header.find("h4", class_="heading")
                #获取标题
                title_tag = header_module.find("a")
                name = title_tag.get_text(strip=True)
                name_url = self.base_url + title_tag["href"]
                #获取作者
                author_tag = header_module.find("a", class_="author")
                author = author_tag.get_text(strip=True)
                author_url = self.base_url + author_tag["href"]
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
                results.append(work_info)
        return results
    
def main():
    #用户输入产品名称
    query = input("Whatsyourfavorite:")
    encoded_query = quote(query)
    #从我的账户进行爬取
    scraper = AO3Scraper()
    html = f"https://archiveofourown.org/works/search?work_search%5Bquery%5D={encoded_query}"
    #得到最大页数
    response = requests.get(html, headers=scraper.headers, cookies=scraper.cookies)
    scraper.max_num = scraper.get_all_pages(response.text)
    if scraper.max_num > 1:
        scraper.search(query)
    else:
        scraper._parse_search_results(html)

if __name__ == "__main__":
    main()
        
