import scraper

def get(config: dict):
	print(scraper.test)
	instance = scraper.Scraperex()
	return instance.get(config)