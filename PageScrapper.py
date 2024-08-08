from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PageScrapper:

    def __init__(self, url, num_of_pages_to_scrap=-1):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )  # Setup Chrome driver
        self.url = url
        self.num_of_pages_to_scrap = (
            num_of_pages_to_scrap  # 0 means to scrap all existing pages
        )

        self.timeout = 5  # Increase timeout to 30 seconds;
        self.additional_timeout = 1  # one second

    def __del__(self):
        self.driver.quit()

    def __load_page(self):
        self.driver.get(self.url)

    def __move_to_next_list_page(self):
        # Try to click the 'next' button to go to the next page
        try:
            next_button = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.pagination__nav-btn--next")
                )
            )
            self.driver.execute_script("arguments[0].click();", next_button)
            # Optionally, wait for the page to load
            time.sleep(self.additional_timeout)
            return True
        except Exception as e:
            print(f"An error occurred while navigating to the next page: {e}")
            return False

    def __get_current_html_page(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "partner-card"))
        )  # Wait until the element is present

        # Give some additional time for JavaScript to render content
        time.sleep(self.additional_timeout)

        # Get the page source after JavaScript has rendered the content
        return self.driver.page_source

    def __get_total_pages(self):
        # if user defined custom number of pages to scrap
        if self.num_of_pages_to_scrap != -1:
            return self.num_of_pages_to_scrap

        total_pages = 0
        try:
            # Find all pagination buttons
            pagination_buttons = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "button.pagination__page-btn")
                )
            )
            # The last pagination button contains the total number of pages
            total_pages = int(pagination_buttons[-1].text.strip())
            print(f"Total pages found: {total_pages}")
        except Exception as e:
            print(f"An error occurred while getting the total number of pages: {e}")
        return total_pages

    def __iterate_through_list(self):
        html_container = ""

        total_pages = self.__get_total_pages()
        for page_num in range(total_pages):  # Adjust the range as needed
            try:
                html_container += self.__get_current_html_page()
                print(f"Collected data from page #{page_num}")
                res = self.__move_to_next_list_page()
                if res == False:
                    break
            except Exception as e:
                print(f"An error occurred while processing page {page_num}: {e}")
                break
        return html_container

    def __save_html_in_file(self, filename, html):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)
        print(f"Rendered HTML from all pages has been saved to '{filename}'")

    def get_partner_link(self, partner_id):
        base = "https://partnersdirectory.withgoogle.com/partners/"
        url = base + partner_id
        self.driver.get(url)
        website_link = None
        try:
            # Wait until the element is present
            link_element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.hero__website-btn"))
            )
            # Get the href attribute of the link element
            website_link = link_element.get_attribute("href")
        except Exception as e:
            print(f"An error occurred while retrieving link: {e}")
        return website_link

    def download_html(self, filename="main.html"):
        try:
            self.__load_page()
            html_pages = self.__iterate_through_list()
            if html_pages != "":
                self.__save_html_in_file(filename, html_pages)
        except Exception as e:
            print(f"An error occurred during scrapping the pages: {e}")

    def get_html(self):
        try:
            self.__load_page()
            html_pages = self.__iterate_through_list()
            return html_pages
        except Exception as e:
            print(f"An error occurred during scrapping the pages: {e}")
        return ""
