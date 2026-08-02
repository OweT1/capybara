from loguru import logger

from .scraper import GreatEasternScraper


def main() -> None:
    scraper = GreatEasternScraper()
    scraper.run_link_extraction()
    logger.info(f"Extracted links and saved to {scraper.policy_links_path}!")


if __name__ == "__main__":
    main()
