import os
import threading
from pathlib import Path
from typing import Any

import requests
import yaml
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

DEFAULT_TIMEOUT = 30

_thread_local = threading.local()


def get_session() -> requests.Session:
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        _thread_local.session = session
    return session


# --- General Helper function --- #
def get_name_from_link(link: str) -> str:
    return Path(link).stem


# --- YAML File Helper functions --- #
def load_yaml_file(file_name: str) -> Any:
    with open(file_name, "r") as f:
        return yaml.safe_load(f)


def save_dict_to_yaml_file(file_name: str, dict_item: dict) -> None:
    with open(file_name, "w") as output_file:
        yaml.dump(dict_item, output_file, sort_keys=False, default_flow_style=False)
    logger.info(f"File contents saved to {file_name}")


# --- BeautifulSoup Scrapping - Static JS --- #
def get_pdf_files_from_webpage(link: str) -> list[str]:
    response = get_session().get(link, timeout=DEFAULT_TIMEOUT)
    if not response.ok:
        raise ValueError(f"Link not working... {link}")

    content = BeautifulSoup(response.text, "html.parser")
    pdf_links = []
    for anchor in content.find_all("a"):
        href = anchor.get("href")
        if href and href.lower().endswith(".pdf"):
            pdf_links.append(href)
    return pdf_links


def download_pdf_file_from_link(
    link: str, category: str, subcategory: str, policy: str
) -> None:
    link_name = get_name_from_link(link)
    output_folder_dir = f"data/raw/{category}/{subcategory}/{policy}"
    output_file_dir = f"{output_folder_dir}/{link_name}.pdf"

    if os.path.exists(output_file_dir):
        logger.info(f"File already exists, skipping: {output_file_dir}")
        return

    try:
        response = get_session().get(link, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Error reading url {link}: {e}"
        ) from e

    os.makedirs(output_folder_dir, exist_ok=True)
    with open(output_file_dir, "wb") as file:
        file.write(response.content)
    logger.info(f"File has been downloaded at {output_file_dir}")


def get_text_from_webpage(link: str) -> str:
    try:
        response = requests.get(link, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Error reading url {link}: {e}"
        ) from e

    content = BeautifulSoup(response.text, "html.parser")
    return content.get_text(strip=True, separator=" ")


# --- Selenium Scrapping - Dynamic JS --- #
def get_web_links_js(link: str) -> list[str]:
    # Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--incognito")

    # Initialise driver
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(link)
        # Finds the web elements with the tag_name and class_name, afterwards converting from WebElement objects to their relevant text
        items = driver.find_elements(
            By.XPATH,
            '//a[@class="leo-button leo-button--outline leo-button--secondary mr-auto"]',
        )
        return [item.get_attribute("href") for item in items]
    finally:
        # Closes the website
        driver.quit()
