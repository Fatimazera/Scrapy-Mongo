import scrapy
from pathlib import Path
from pymongo import MongoClient
import certifi
import datetime

from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

# uri = "mongodb+srv://test:test12345@cluster0.ql14h8k.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print("Connection failed:", e)
db = client.scrapy
def inserttomongo(page,title,rating,price,image,instock):
    collection = db[page]
    doc = {
    "title": title,
    "rating": rating,
    "price": price,
    "image" : image,
    "instock" : instock,
    "date" : datetime.datetime.utcnow()
}
    inserted = collection.insert_one(doc)
    return inserted.inserted_id


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]


    async def start(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log(f"Processing page {page}")

        cards = response.css('.product_pod')

        for card in cards:
            title = card.css("h3 > a::text").get(default="")

            rating_class = card.css(".star-rating::attr(class)").get(default="")
            rating = rating_class.split()[-1] if rating_class else ""

            price = card.css(".price_color::text").get(default="")

            image = card.css(".image_container img::attr(src)").get(default="")
            image = response.urljoin(image)

            instock = bool(card.css(".icon-ok"))

            inserttomongo(page, title, rating, price, image, instock)


