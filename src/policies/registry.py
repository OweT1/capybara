"""Registry of provider scrapers.

New insurance providers register their ``PolicyScraper`` subclass with the
``@register`` decorator, after which they can be looked up by name for
provider-agnostic orchestration (e.g. an Airflow DAG iterating over all
providers).
"""

from __future__ import annotations

from .base import PolicyScraper

_registry: dict[str, type[PolicyScraper]] = {}


def register(scraper_cls: type[PolicyScraper]) -> type[PolicyScraper]:
    """Class decorator registering a provider scraper under its name."""
    _registry[scraper_cls.provider_name] = scraper_cls
    return scraper_cls


def get_scraper(provider_name: str) -> PolicyScraper:
    """Instantiate the registered scraper for ``provider_name``."""
    try:
        return _registry[provider_name]()
    except KeyError:
        raise KeyError(f"No scraper registered for provider: {provider_name}") from None


def available_scrapers() -> list[str]:
    return sorted(_registry)
