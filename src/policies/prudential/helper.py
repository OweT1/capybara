import yaml
import sys, os

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from loguru import logger

# --- General Helper function --- #
def get_name_from_link(link):
  return link.split("/")[-1].split(".")[0]

# --- YAML File Helper functions --- #
def load_yaml_file(file):
  with open(file, 'r') as f:
    file_content = yaml.safe_load(f)
  return file_content

def save_dict_to_yaml_file(file, dict_item):
  with open(file, 'w') as output_file:
    yaml.dump(dict_item, output_file, sort_keys=False, default_flow_style=False)
  logger.info(f"File contents saved to {file}")

# --- BeautifulSoup Scrapping - Static JS --- #
def get_web_links(link):
  response = requests.get(link)
  if response.ok:
    content = BeautifulSoup(response.text, 'html.parser')
    links_content = content.find_all("a", "leo-button leo-button--outline leo-button--secondary mr-auto")
    links = [link_content["href"] for link_content in links_content]
  else:
    links = []
    raise ValueError("Link not working...")
  return links

def get_pdf_files_from_webpage(link):
  response = requests.get(link)
  pdf_links = []
  if response.ok:
    content = BeautifulSoup(response.text, 'html.parser')
    links = content.find_all("a")
    for link in links:
      href = link.get("href")
      if href and href.lower().endswith(".pdf"):
        pdf_links.append(href)
  return pdf_links

def download_pdf_file_from_link(link, category, subcategory, policy):
  try:
    response = requests.get(link)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    logger.error(f"Error reading url: {e}")
    exit()
  
  link_name = get_name_from_link(link)
  output_folder_dir = f"data/raw/{category}/{subcategory}/{policy}"
  os.makedirs(output_folder_dir, exist_ok=True)
  output_file_dir = f"{output_folder_dir}/{link_name}.pdf"
  with open(output_file_dir, "wb") as file:
    file.write(response.content)
  logger.info(f"File has been downloaded at {output_file_dir}")

def get_text_from_webpage(link):
  try:
    response = requests.get(link)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    logger.error(f"Error reading url: {e}")
    exit()
    
  content = BeautifulSoup(response.text, 'html.parser')
  full_text = content.get_text(strip=True, separator=" ")
  return full_text

# --- Selenium Scrapping - Dynamic JS --- #
def get_web_links_js(link):
  # Chrome Options
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--disable-web-security")
  chrome_options.add_argument("--incognito")
  
  # Initialise driver
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(link)
  
  # Finds the web elements with the tag_name and class_name, afterwards converting from WebElement objects to their relevant text
  items = driver.find_elements(By.XPATH, f'//a[@class="leo-button leo-button--outline leo-button--secondary mr-auto"]')
  items = [item.get_attribute("href") for item in items]
  
  # Closes the website
  driver.close()
  
  return items
