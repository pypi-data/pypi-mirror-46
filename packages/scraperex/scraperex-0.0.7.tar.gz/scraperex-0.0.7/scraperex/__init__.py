from scraperex.scraper import Scraper

def get(config: dict):
	scraper = Scraper()
	return scraper.get(config)