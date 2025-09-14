from bs4 import BeautifulSoup
from item_scraper import AO3Scraper

ao3_scraper = AO3Scraper()
class TagScraper():
    def __init__(self):
        self.tag_text_list = []
        self.tag_result_list = []
        for result in ao3_scraper.results:
            for tag in result["tags"]:
                self.tag_text_list.append(tag["text"])
    
    def get_tag_list(self):
        for tag_name in self.tag_text_list:
            result = []
            result = ao3_scraper.html_conn(tag_name)
            self.tag_result_list.append(result)
        return True
if __name__ =="main":
    tag_scraper = TagScraper()
    tag_scraper.get_tag_list()
