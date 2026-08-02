from concurrent.futures import ThreadPoolExecutor
from typing import Any
from urllib.parse import urljoin

from loguru import logger

from .constants import PRUDENTIAL_POLICY_LINKS_PATH
from .helper import (
    download_pdf_file_from_link,
    get_pdf_files_from_webpage,
    load_yaml_file,
)

MAX_WORKERS = 8


def _download_pdf_file(task: tuple[str, str, str, str]) -> None:
    full_pdf_link, category, subcategory, policy = task
    try:
        download_pdf_file_from_link(full_pdf_link, category, subcategory, policy)
    except Exception as e:  # noqa: BLE001 - keep one bad download from failing the whole batch
        logger.error(f"Failed to download {full_pdf_link}: {e}")


def extract_pdf_from_links(links: dict) -> None:
    download_tasks: list[tuple[str, str, str, str]] = []
    for categories in links.values():
        company_url = categories["base_url"]
        for category, subcategories in categories["policies"].items():
            for subcategory, policies in subcategories.items():
                for policy, policy_content in policies.items():
                    policy_link = policy_content["link"]
                    pdf_links = list(set(get_pdf_files_from_webpage(policy_link)))
                    for pdf_link in pdf_links:
                        full_pdf_link = urljoin(company_url, pdf_link)
                        download_tasks.append(
                            (full_pdf_link, category, subcategory, policy)
                        )

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(_download_pdf_file, download_tasks)


def main():
    logger.info("Loading and extracting PDF files from links...")
    links: Any = load_yaml_file(PRUDENTIAL_POLICY_LINKS_PATH)
    extract_pdf_from_links(links)
    logger.info("Completed extraction of PDF files from links!")


if __name__ == "__main__":
    main()
