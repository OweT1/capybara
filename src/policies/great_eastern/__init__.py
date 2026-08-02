from .file_extraction import main as extract_files
from .link_extraction import main as extract_links
from .scraper import GreatEasternScraper

__all__ = ["GreatEasternScraper", "extract_files", "extract_links"]
