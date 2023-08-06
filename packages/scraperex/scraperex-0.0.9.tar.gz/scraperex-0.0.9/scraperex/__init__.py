import scraper

def get(config: dict):
	instance = Scraper()
	return instance.get(config)