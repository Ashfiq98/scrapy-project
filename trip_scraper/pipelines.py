import os
import requests
from sqlalchemy.exc import SQLAlchemyError
from trip_scraper.models import session, Hotel


class HotelPipeline:
    IMAGE_DIR = "trip_scraper/images"
    OUTPUT_FILE = "outputs.json"

    def open_spider(self, spider):
        os.makedirs(self.IMAGE_DIR, exist_ok=True)
        # Clear JSON file
        if os.path.exists(self.OUTPUT_FILE):
            with open(self.OUTPUT_FILE, "w") as file:
                file.write("")  # Empty the file
            spider.logger.info(f"Cleared the {self.OUTPUT_FILE} file.")
        else:
            spider.logger.info(f"{self.OUTPUT_FILE} does not exist. A new file will be created.")

        # Clear database
        try:
            session.query(Hotel).delete()  # Deletes all records
            session.commit()
            spider.logger.info("Database cleared successfully.")
        except SQLAlchemyError as e:
            spider.logger.error(f"Error clearing database: {e}")
            session.rollback()

    def process_item(self, item, spider):
        # Save the image locally
        image_url = item.get("image_url")
        image_path = None
        if image_url:
            try:
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    image_name = f"{item['hotel_title'].replace(' ', '_')}.jpg"
                    image_path = os.path.join(self.IMAGE_DIR, image_name)
                    with open(image_path, "wb") as img_file:
                        img_file.write(response.content)
            except Exception as e:
                spider.logger.error(f"Error downloading image for {item['hotel_title']}: {e}")

        # Add the item to the database
        try:
            hotel_record = Hotel(
                hotel_title=item.get("hotel_title", "Unknown"),
                rating=item.get("rating", None),
                location=item.get("location", "Unknown"),
                latitude=item.get("latitude", None),
                longitude=item.get("longitude", None),
                room_type=item.get("room_type", "Unknown"),
                price=item.get("price", None),
                image_url=image_path,
            )
            session.add(hotel_record)
            session.commit()
        except SQLAlchemyError as e:
            spider.logger.error(f"Database error: {e}")
            session.rollback()

        return item
