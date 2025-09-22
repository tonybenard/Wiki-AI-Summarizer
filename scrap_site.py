from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class WikipediaScraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def parse_site(self, site_url, search):
        self.driver.get(site_url)

        # Search box interaction
        research = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "searchInput"))
        )
        research.send_keys(search, Keys.ENTER)

        # Wait for results page to load
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, 'bodyContent'))
        )

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        body = soup.find("div", id='bodyContent')

        if not body:
            return {"title": "No title found", "content": ""}

        # Remove unwanted tags
        for unwanted in body.find_all(["script", "style", "img", "input", "nav", "figure", "table", "button"]):
            unwanted.decompose()

        title = soup.title.string if soup.title else "No title found"
        content = body.get_text(" ", strip=True)

        return {"title": title, "content": content}
        
    
    def close(self):
        self.driver.quit()        