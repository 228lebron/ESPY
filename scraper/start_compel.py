from scrapy.crawler import CrawlerProcess
#from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings as Settings
from scraper.spiders.compel_by_zero_days_priority import CompelZeroDaysSpider

settings = Settings()
process = CrawlerProcess(settings=Settings())
process.crawl(CompelZeroDaysSpider)
process.start()