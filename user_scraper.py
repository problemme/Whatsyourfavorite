from bs4 import BeautifulSoup
from item_scraper import AO3Scraper
import requests

scraper = AO3Scraper()
# 抓取时选择距离li标签最近的那个div
class AuthorScraper:
    def __init__(self):
        self.results = scraper.results
        self.work_list = {}
        self.author_url_list = [item["author"]["url"] for item in self.results]

    def get_work_list(self):
        for url in self.author_url_list:
            headers = {"User-Agent": "Chrome",
                       "Cookie": f"_otwarchive_session=eyJfcmFpbHMiOnsibWVzc2FnZSI6ImV5SnpaWE56YVc5dVgybGtJam9pTXpFek5tWmxaakZrTm1GbU9ERTNabUV4TW1aaVpqZzRPVEJqTTJVeE56RWlMQ0ozWVhKa1pXNHVkWE5sY2k1MWMyVnlMbXRsZVNJNlcxc3lNelV6TmpneE0xMHNJaVF5WVNReE5DUkJaekYxUlRKTE1HbHpVVUUxZGxKTVEyMXhPRGRsSWwwc0luSmxkSFZ5Ymw5MGJ5STZJaTkxYzJWeWN5OVVhR1ZrYjNOcFlTSXNJbDlqYzNKbVgzUnZhMlZ1SWpvaWVuUk5iRGw2TlY5YWJESXpOWFI1YmtWcmExazRhM0EzYjBwalVteFJSV2xKTXpVeE5GQmhYMGxLY3lKOSIsImV4cCI6IjIwMjUtMDgtMjNUMDU6MzM6MzguMzgxWiIsInB1ciI6ImNvb2tpZS5fb3R3YXJjaGl2ZV9zZXNzaW9uIn19--2d22e0e5ce95447bc994873910afb3f652597617"}
            responce = requests.get(url, headers = headers, timeout = 60)
            responce.raise_for_status()
            soup = BeautifulSoup(responce.text, "lxml")
            work_items = soup.select("li.work.blurb.group")
            for item in work_items:
                div_header = item.find("div", class_="header module")
                header_module = div_header.find("h4", class_="heading")
                title = header_module.find("a", href = True)
                title_name = title.get_text(strip = True)
                title_url = scraper.base_url + title["href"]
                self.work_list[title_name] = title_url
        return True
    
if __name__ == "main":
    scraper = AuthorScraper()
    scraper.get_work_list()
