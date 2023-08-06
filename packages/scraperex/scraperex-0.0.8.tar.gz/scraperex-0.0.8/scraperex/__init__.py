from .scraper import Scraper

def get(config: dict):
	scraper = Scraper()
	return scraper.get(config)