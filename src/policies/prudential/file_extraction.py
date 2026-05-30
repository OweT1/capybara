from loguru import logger
from urllib.parse import urljoin

from .helper import (
  download_pdf_file_from_link,
  load_yaml_file,
  get_pdf_files_from_webpage,
  get_text_from_webpage,
  get_name_from_link,
)

def extract_pdf_from_links(links):
  for company, categories in links.items():
    company_url = categories["base_url"]
    for category, subcategories in categories["policies"].items():
      for subcategory, policies in subcategories.items():
        for policy, policy_content in policies.items():
          policy_link = policy_content["link"]
          pdf_links = list(set(get_pdf_files_from_webpage(policy_link)))
          for pdf_link in pdf_links:
            full_pdf_link = urljoin(company_url, pdf_link)
            download_pdf_file_from_link(full_pdf_link, category, subcategory, policy)

def main():
  logger.info("Loading and extracting PDF files from links...")
  links = load_yaml_file("src/services/data_extraction/policy_webpage_links.yaml")
  extract_pdf_from_links(links)
  logger.info("Completed extraction of PDF files from links!")

if __name__ == "__main__":
  main()
  