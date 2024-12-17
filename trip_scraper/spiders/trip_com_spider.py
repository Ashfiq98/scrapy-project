# trip_com_spider.py
import scrapy
import json
import re
import random
import os


class ScraperSpider(scrapy.Spider):
    name = "trip_com_spider"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract script containing data
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            self.log("Found script containing `window.IBU_HOTEL` data.")

            # Extract JSON-like data using regex
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', ibu_hotel_data, re.DOTALL)

            if match:
                try:
                    json_string = match.group(1)
                    data = json.loads(json_string)

                    # Extract `htlsData`
                    htls_data = data.get("initData", {}).get("htlsData", {})
                    if htls_data:
                        inbound_cities = htls_data.get("inboundCities", [])
                        if inbound_cities:
                            # Process only the first city to get its ID
                            # index = self.generate_random_index(len(inbound_cities))
                            city = inbound_cities[0]
                            city_id = city.get("id", "")  # Get the city ID

                            # Generate the URL using the city ID
                            city_url = f"https://uk.trip.com/hotels/list?city={city_id}"

                            # After getting the city_id, we can crawl hotels using this URL
                            yield scrapy.Request(url=city_url, callback=self.parse_hotels, meta={'city_id': city_id})

                        else:
                            self.logger.error("No 'inboundCities' found in 'htlsData'.")
                        # Handle outbound cities
                        outbound_cities = htls_data.get("outboundCities", [])
                        if outbound_cities:
                            # index = self.generate_random_index(len(outbound_cities))
                            city = outbound_cities[0]
                            city_id = city.get("id", "")
                            city_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                            yield scrapy.Request(url=city_url, callback=self.parse_hotels, meta={'city_id': city_id})
                        else:
                            self.logger.error("No 'outboundCities' found in 'htlsData'.")
                    else:
                        self.logger.error("No 'htlsData' found in 'initData'.")
                except Exception as e:
                    self.log(f"Error parsing JSON data: {e}")
            else:
                self.log("Regex did not match any `window.IBU_HOTEL` data.")
        else:
            self.log("No script containing `window.IBU_HOTEL` data found.")

    def parse_hotels(self, response):
        # Get the city_id from meta data
        city_id = response.meta['city_id']
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if ibu_hotel_data:
            self.log(f"Found hotel data for city ID: {city_id}")

            # Extract JSON-like data using regex
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', ibu_hotel_data, re.DOTALL)

            if match:
                try:
                    json_string = match.group(1)
                    data = json.loads(json_string)

                    # Extract hotel list from initData
                    hotel_list = data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])
                    for hotel in hotel_list:
                        hotel_data = {
                            "hotel_title": hotel.get("hotelBasicInfo", {}).get("hotelName", ""),
                            "rating": hotel.get("commentInfo", {}).get("commentScore", ""),
                            "location": hotel.get("positionInfo", {}).get("positionName", ""),
                            "latitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lat", ""),
                            "longitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lng", ""),
                            "room_type": hotel.get("roomInfo", {}).get("physicalRoomName", ""),
                            "price": hotel.get("hotelBasicInfo", {}).get("price", ""),
                            "image_url": hotel.get("hotelBasicInfo", {}).get("hotelImg", "")
                        }
                        yield hotel_data
                except Exception as e:
                    self.log(f"Error parsing hotel data: {e}")
            else:
                self.log(f"Regex did not match any `window.IBU_HOTEL` data for city ID: {city_id}.")
        else:
            self.log(f"No script containing `window.IBU_HOTEL` data found for city ID: {city_id}.")

    def generate_random_index(self, length):
        return random.randint(0, length - 1)
