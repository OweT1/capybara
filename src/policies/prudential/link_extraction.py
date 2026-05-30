import os, sys
from loguru import logger

from .helper import (
  load_yaml_file,
  save_dict_to_yaml_file,
  get_name_from_link,
  get_web_links,
  get_web_links_js
)

def extract_policy_links_from_category_webpage(category_links):
  output = {}
  for company, files in category_links.items():
    company_url = files['base_url']
    for category, subcategories in files['policies'].items():
      for subcategory, subcategory_content in subcategories.items():
        if company not in output:
          output[company] = {}
        if "base_url" not in output[company]:
          output[company]["base_url"] = company_url
        if "policies" not in output[company]:
          output[company]["policies"] = {}   
        if category not in output[company]["policies"]:
          output[company]["policies"][category] = {}
        if subcategory not in output[company]["policies"][category]:
          output[company]["policies"][category][subcategory] = {}
          
        subcategory_link = subcategory_content['link']
        policy_links = get_web_links_js(subcategory_link)
        for policy_link in policy_links:
          policy_name = get_name_from_link(policy_link)
          if policy_name not in output[company]["policies"][category][subcategory]:
            output[company]["policies"][category][subcategory][policy_name] = {}
          output[company]["policies"][category][subcategory][policy_name]['link'] = policy_link
  return output

def main():
  logger.info("Extracting links from webpage...")
  category_webpage_dict = load_yaml_file('src/services/data_extraction/category_webpage_links.yaml')  
  policy_webpage_links = extract_policy_links_from_category_webpage(category_webpage_dict)
  
  file_output_path = "src/services/data_extraction/policy_webpage_links.yaml"
  save_dict_to_yaml_file(file_output_path, policy_webpage_links)
  logger.info("Extracted links and saved to {}!", file_output_path)

if __name__ == "__main__":
  main()
  
  # Tester code
  # sample_link = 'https://www.greateasternlife.com/sg/en/personal-insurance/our-products.html?category=corp-site%3Aproduct-category%2Fnational-schemes&online=&gift=&keyword='
  # print(get_web_links_js(sample_link))