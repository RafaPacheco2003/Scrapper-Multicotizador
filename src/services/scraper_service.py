import logging
from typing import Dict, Any
from scrapers.implementations.hdi_scraper import hdi_scraper
from scrapers.implementations.mapfre_scraper import mapfre_scraper
from src.services.extendScrapers.scraper_mapfre import MapfreScraperStrategy
from src.services.extendScrapers.scraper_hdi import HdiScraperStrategy


class ScraperService:
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.scrapers = {
            "mapfre": mapfre_scraper,
            "hdi": hdi_scraper,
        }
        self.strategies = {
            "mapfre": MapfreScraperStrategy(),
            "hdi": HdiScraperStrategy(),
        }
    
    async def scrape(self, scraper_name: str, params: Dict[str, Any], extract_data: bool = True) -> Dict[str, Any]:
        name = scraper_name.lower()
        scraper = self.scrapers[name]
        strategy = self.strategies[name]
        
        self.logger.info(f"SCRAPER: {scraper_name.upper()} | Estrategia: {strategy.__class__.__name__}")
        
        url = strategy.prepare_url(params)
        scraped_data = await scraper.scrape(url) if extract_data else None
        
        return {
            "success": True,
            "message": "Completado",
            "scraper_name": scraper_name,
            "url": url or strategy.get_base_url(),
            "data": scraped_data
        }


scraper_service = ScraperService()
