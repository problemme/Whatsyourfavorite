from bs4 import BeautifulSoup
from item_scraper import AO3Scraper

class TagScraper():
    def __init__(self):
        scraper = AO3Scraper()
        self.tag_text_list = []
        self.tag_result_list = []
        for result in scraper.results:
            for tag in result["tags"]:
                self.tag_text_list.append(tag["text"])
    
    def get_tag_list(self):
        scraper = AO3Scraper()
        for tag_name in self.tag_text_list:
            result = []
            result = scraper.html_conn(tag_name)
            self.tag_result_list.append(result)
        return True
if __name__ =="main":
    scraper = TagScraper()
    scraper.get_tag_list()
