from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scraper.spiders.compel_by_zero_days_priority import CompelZeroDaysSpider

settings = Settings()
process = CrawlerProcess(settings=settings)
process.crawl(CompelZeroDaysSpider)
process.start()