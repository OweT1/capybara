from .scraper import GreatEasternScraper


def main() -> None:
    scraper = GreatEasternScraper()
    scraper.run_file_extraction()


if __name__ == "__main__":
    main()
