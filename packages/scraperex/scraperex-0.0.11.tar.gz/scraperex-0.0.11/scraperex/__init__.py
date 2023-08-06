from __future__ import absolute_import, unicode_literals

from scraperex.scraper import Scraper, Scraperex

def get(config: dict):
	instance = Scraper()
	return instance.get(config)