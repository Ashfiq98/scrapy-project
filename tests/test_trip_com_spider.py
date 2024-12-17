import pytest
import scrapy
from scrapy.http import HtmlResponse
import json
import os
import sys
from trip_scraper.spiders.trip_com_spider import ScraperSpider

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def create_mock_response(url, body, meta=None):
    """Create a mock Scrapy response for testing."""
    request = scrapy.Request(url=url, meta=meta or {})
    return HtmlResponse(
        url=url,
        body=body.encode('utf-8'),
        encoding='utf-8',
        request=request  # Tie the response to the request
    )


def test_spider_init():
    """Test basic spider initialization."""
    spider = ScraperSpider()
    assert spider.name == "trip_com_spider"
    assert spider.start_urls == ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]


def test_parse_method_with_valid_data(mocker):
    """Test parse method with mock valid JSON data."""
    # Mock data similar to what might be found in window.IBU_HOTEL
    mock_json_data = {
        "initData": {
            "htlsData": {
                "inboundCities": [
                    {
                        "id": "12345",
                        "name": "London"
                    }
                ],
                "outboundCities": [
                    {
                        "id": "67890",
                        "name": "Paris"
                    }
                ]
            }
        }
    }
    
    # Create a script tag with mock data
    mock_script_content = f"window.IBU_HOTEL = {json.dumps(mock_json_data)};"
    
    # Create mock response
    mock_response = create_mock_response(
        "https://uk.trip.com/hotels/?locale=en-GB&curr=GBP",
        f"<html><script>{mock_script_content}</script></html>"
    )
    
    # Create spider instance
    spider = ScraperSpider()
    
    # Collect generated requests
    requests = list(spider.parse(mock_response))
    
    # Assert we get two requests (one for inbound, one for outbound city)
    assert len(requests) == 2
    assert all(isinstance(req, scrapy.Request) for req in requests)
    assert requests[0].url == "https://uk.trip.com/hotels/list?city=12345"
    assert requests[1].url == "https://uk.trip.com/hotels/list?city=67890"

def test_parse_hotels_method(mocker):
    """Test parse_hotels method with mock hotel data."""
    mock_hotel_data = {
        "initData": {
            "firstPageList": {
                "hotelList": [
                    {
                        "hotelBasicInfo": {
                            "hotelName": "Test Hotel",
                            "price": 100.50,
                            "hotelImg": "http://example.com/hotel.jpg"
                        },
                        "commentInfo": {
                            "commentScore": 4.5
                        },
                        "positionInfo": {
                            "positionName": "City Center",
                            "coordinate": {
                                "lat": 51.5074,
                                "lng": -0.1278
                            }
                        },
                        "roomInfo": {
                            "physicalRoomName": "Double Room"
                        }
                    }
                ]
            }
        }
    }
    
    # Create a script tag with mock data
    mock_script_content = f"window.IBU_HOTEL = {json.dumps(mock_hotel_data)};"
    
    # Create mock response
    mock_response = create_mock_response(
        "https://uk.trip.com/hotels/list?city=12345",
        f"<html><script>{mock_script_content}</script></html>"
    )
    mock_response.meta['city_id'] = '12345'
    
    # Create spider instance
    spider = ScraperSpider()
    
    # Collect generated items
    items = list(spider.parse_hotels(mock_response))
    
    # Assert correct item extraction
    assert len(items) == 1
    hotel = items[0]
    assert hotel['hotel_title'] == "Test Hotel"
    assert hotel['rating'] == 4.5
    assert hotel['location'] == "City Center"
    assert hotel['latitude'] == 51.5074
    assert hotel['longitude'] == -0.1278
    assert hotel['room_type'] == "Double Room"
    assert hotel['price'] == 100.50
    assert hotel['image_url'] == "http://example.com/hotel.jpg"

def test_generate_random_index():
    """Test the random index generation method."""
    spider = ScraperSpider()
    
    # Test for various list lengths
    for length in [1, 5, 10, 100]:
        index = spider.generate_random_index(length)
        assert 0 <= index < length, f"Index out of range for length {length}"