from bs4 import BeautifulSoup
from item_scraper import AO3Scraper

# 抓取时选择距离li标签最近的那个div
class AuthorScraper:
    def __init__(self):
        scraper = AO3Scraper()
        self.results = scraper.results
        self.work_list = {}
        self.author_url_list = [item["author"]["url"] for item in self.results]

    def get_work_list(self):
        scraper = AO3Scraper()
        for html in self.author_url_list:
            soup = BeautifulSoup(html, "lxml")
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
