"""Base class for insurance-provider policy scrapers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from loguru import logger

from .common.http import DEFAULT_TIMEOUT, download_file, get_session
from .common.paths import build_download_path, get_name_from_link
from .common.yaml_utils import load_yaml_file, save_dict_to_yaml_file

DEFAULT_MAX_WORKERS = 8


class PolicyScraper(ABC):
    """Scrapes and downloads policy documents for a single insurance provider.

    Subclasses configure provider-specific details (base URL, YAML file paths,
    selectors) and implement how policy pages are discovered. Generic tree
    walking, PDF discovery and parallel download logic live here.
    """

    provider_name: str
    base_url: str
    category_links_path: str
    policy_links_path: str
    raw_output_root: str = "data/raw"
    max_workers: int = DEFAULT_MAX_WORKERS

    def __init__(self) -> None:
        self.session = get_session()

    @abstractmethod
    def extract_policy_links_from_category_page(
        self, subcategory_link: str
    ) -> list[str]:
        """Return policy page URLs found on a subcategory page."""

    def extract_pdf_links_from_policy_page(self, policy_link: str) -> list[str]:
        """Return PDF URLs found on a policy page (default: anchors ending in .pdf)."""
        logger.debug(f"[{self.provider_name}] Scraping PDF links from {policy_link}")
        response = self.session.get(policy_link, timeout=DEFAULT_TIMEOUT)
        if not response.ok:
            raise ValueError(f"Link not working... {policy_link}")

        content = BeautifulSoup(response.text, "html.parser")
        pdf_links = []
        for anchor in content.find_all("a"):
            href = anchor.get("href")
            if href and href.lower().endswith(".pdf"):
                pdf_links.append(href)
        return pdf_links

    @staticmethod
    def _count_policies(policy_links: dict) -> int:
        """Return the total number of policies in a policy links tree."""
        return sum(
            len(subcategory_policies)
            for company in policy_links.values()
            for category in company["policies"].values()
            for subcategory_policies in category.values()
        )

    # --- Link extraction --- #
    def extract_policy_links(self, category_links: dict) -> dict:
        """Walk the category tree and scrape policy links for every subcategory."""
        output: dict = {}
        for company, files in category_links.items():
            company_node = output.setdefault(
                company, {"base_url": files["base_url"], "policies": {}}
            )
            for category, subcategories in files["policies"].items():
                category_node = company_node["policies"].setdefault(category, {})
                for subcategory, subcategory_content in subcategories.items():
                    subcategory_node = category_node.setdefault(subcategory, {})
                    subcategory_link = subcategory_content["link"]
                    logger.info(
                        f"[{self.provider_name}] Scraping subcategory '{subcategory}' ({category})"
                    )
                    for policy_link in self.extract_policy_links_from_category_page(
                        subcategory_link
                    ):
                        policy_name = get_name_from_link(policy_link)
                        subcategory_node.setdefault(policy_name, {})["link"] = (
                            policy_link
                        )
                    logger.info(
                        f"[{self.provider_name}] Found {len(subcategory_node)} policy link(s) for subcategory '{subcategory}'"
                    )
        return output

    def run_link_extraction(self) -> None:
        """Scrape policy page links and save them to the policy links YAML."""
        logger.info(f"[{self.provider_name}] Extracting links from webpage...")
        category_links = load_yaml_file(self.category_links_path)
        logger.info(
            f"[{self.provider_name}] Loaded {len(category_links)} provider(s) from {self.category_links_path}"
        )
        policy_links = self.extract_policy_links(category_links)
        total_policies = self._count_policies(policy_links)
        logger.info(
            f"[{self.provider_name}] Extracted {total_policies} policy link(s) in total"
        )
        save_dict_to_yaml_file(self.policy_links_path, policy_links)

    # --- File extraction --- #
    def _download_pdf(self, task: tuple[str, str]) -> None:
        link, output_path = task
        logger.debug(f"[{self.provider_name}] Downloading {link} to {output_path}")
        try:
            download_file(self.session, link, output_path)
        except Exception as e:  # noqa: BLE001 - keep one bad download from failing the whole batch
            logger.error(f"Failed to download {link}: {e}")

    def extract_pdf_files(self, policy_links: dict) -> None:
        """Walk the policy tree, discover PDF links and download them in parallel."""
        download_tasks: list[tuple[str, str]] = []
        for categories in policy_links.values():
            company_url = categories["base_url"]
            for category, subcategories in categories["policies"].items():
                for subcategory, policies in subcategories.items():
                    for policy, policy_content in policies.items():
                        policy_link = policy_content["link"]
                        logger.debug(
                            f"[{self.provider_name}] Scraping PDFs for policy '{policy}' ({category}/{subcategory})"
                        )
                        pdf_links = list(
                            set(self.extract_pdf_links_from_policy_page(policy_link))
                        )
                        logger.debug(
                            f"[{self.provider_name}] Found {len(pdf_links)} PDF link(s) for policy '{policy}'"
                        )
                        for pdf_link in pdf_links:
                            full_pdf_link = urljoin(company_url, pdf_link)
                            output_path = build_download_path(
                                self.raw_output_root,
                                category,
                                subcategory,
                                policy,
                                full_pdf_link,
                            )
                            download_tasks.append((full_pdf_link, output_path))

        logger.info(
            f"[{self.provider_name}] Queued {len(download_tasks)} PDF download(s)"
        )
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._download_pdf, download_tasks)

    def run_file_extraction(self) -> None:
        """Discover and download PDF files for all policies in the policy links YAML."""
        logger.info(
            f"[{self.provider_name}] Loading and extracting PDF files from links..."
        )
        policy_links = load_yaml_file(self.policy_links_path)
        total_policies = self._count_policies(policy_links)
        logger.info(
            f"[{self.provider_name}] Loaded {total_policies} policy page(s) from {self.policy_links_path}"
        )
        self.extract_pdf_files(policy_links)
        logger.info(
            f"[{self.provider_name}] Completed extraction of PDF files from links!"
        )
