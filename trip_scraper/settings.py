# Scrapy settings for trip_scraper project

BOT_NAME = "trip_scraper"

SPIDER_MODULES = ["trip_scraper.spiders"]
NEWSPIDER_MODULE = "trip_scraper.spiders"
FEEDS = {
    "outputs.json": {
        "format": "json",
        "overwrite": True,  # Ensures the file is cleared before each run
    }
}
# FEED_FORMAT = 'json'
# FEED_URI = 'outputs.json'
IMAGES_STORE = "trip_scraper/images"  # Path to store downloaded images

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "trip_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 4

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
#SPIDER_MIDDLEWARES = {
#    "trip_scraper.middlewares.TripScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
#DOWNLOADER_MIDDLEWARES = {
#    "trip_scraper.middlewares.TripScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
ITEM_PIPELINES = {
   "trip_scraper.pipelines.HotelPipeline": 300,
   'scrapy.pipelines.images.ImagesPipeline': 1,  # Image pipeline to download hotel images
}

# Database URL for connecting to PostgreSQL (adjust based on your actual DB URL)
DATABASE_URL = "postgresql://user:password@db/mydb"  # PostgreSQL connection string

# Enable and configure the AutoThrottle extension (disabled by default)
#AUTOTHROTTLE_ENABLED = True
#AUTOTHROTTLE_START_DELAY = 5
#AUTOTHROTTLE_MAX_DELAY = 60
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
