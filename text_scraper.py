from item_scraper import AO3Scraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ao3_scraper = AO3Scraper()

class TextScraper():
    def __init__(self):
        self.full_text_list = []

    def get_text_list(self, url):
        # for result in scraper.results:
        #     #获取第一页的链接
        #     url = result["title"]["url"]
        driver = webdriver.Chrome()
        driver.get("https://archiveofourown.org/")
        driver.add_cookie({
            "name": "_otwarchive_session",
            "value": "eyJfcmFpbHMiOnsibWVzc2FnZSI6ImV5SnpaWE56YVc5dVgybGtJam9pTXpFek5tWmxaakZrTm1GbU9ERTNabUV4TW1aaVpqZzRPVEJqTTJVeE56RWlMQ0ozWVhKa1pXNHVkWE5sY2k1MWMyVnlMbXRsZVNJNlcxc3lNelV6TmpneE0xMHNJaVF5WVNReE5DUkJaekYxUlRKTE1HbHpVVUUxZGxKTVEyMXhPRGRsSWwwc0luSmxkSFZ5Ymw5MGJ5STZJaTkxYzJWeWN5OVVhR1ZrYjNOcFlTSXNJbDlqYzNKbVgzUnZhMlZ1SWpvaWVuUk5iRGw2TlY5YWJESXpOWFI1YmtWcmExazRhM0EzYjBwalVteFJSV2xKTXpVeE5GQmhYMGxLY3lKOSIsImV4cCI6IjIwMjUtMDgtMjNUMDU6MzM6MzguMzgxWiIsInB1ciI6ImNvb2tpZS5fb3R3YXJjaGl2ZV9zZXNzaW9uIn19--2d22e0e5ce95447bc994873910afb3f652597617",
            "domain": ".archiveofourown.org"
        })
        driver.get(url)
        full_text = []
        # 开始循环获取文本
        while True:
            WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "workskin")))
            # get_attribute取出了workskin这一标签里所有的HTML
            page_one = driver.find_element(By.ID, "workskin").get_attribute("innerHTML")
            full_text.append(page_one)
            # 翻页
            next_page = driver.find_elements(By.CSS_SELECTOR, 'ul.actions[role="navigation"] li:nth-of-type(2) a')
            if next_page:
                # 获取下一页的子链接
                next_link = next_page.__getattribute__("href")
                driver.get(ao3_scraper.base_url + next_link)
            else:
                break
        driver.quit()
        return full_text
if __name__ ==  'main':
    url = " "
    text_scraper = TextScraper()
    text_scraper.get_text_list(url)
