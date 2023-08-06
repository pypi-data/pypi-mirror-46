from .scraper import Scraperex

def find(config: dict):
	scraper = Scraperex()
	return scraper.get(config)