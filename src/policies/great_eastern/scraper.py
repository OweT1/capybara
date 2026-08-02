"""Great Eastern policy scraper."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from ..base import PolicyScraper
from ..registry import register


@register
class GreatEasternScraper(PolicyScraper):
    provider_name = "great_eastern"
    base_url = "https://www.greateasternlife.com"
    category_links_path = "data/policies/great_eastern/category_webpage_links.yaml"
    policy_links_path = "data/policies/great_eastern/policy_webpage_links.yaml"
    policy_link_xpath = (
        '//a[@class="leo-button leo-button--outline leo-button--secondary mr-auto"]'
    )

    def extract_policy_links_from_category_page(
        self, subcategory_link: str
    ) -> list[str]:
        """Policy page links are rendered by JavaScript, so scrape with Selenium."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--incognito")

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(subcategory_link)
            items = driver.find_elements(By.XPATH, self.policy_link_xpath)
            return [item.get_attribute("href") for item in items]
        finally:
            driver.quit()
