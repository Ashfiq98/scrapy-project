import scrapy

class TripScraperItem(scrapy.Item):
    hotel_title = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    room_type = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()  # Add this for the hotel image URL
