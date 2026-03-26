from pymongo import MongoClient
import certifi
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
posts = db.test_collection

doc = post = {
    "title": "Atomic Habits",
    "price": 499,
    "rating": 5
}
post_id = posts.insert_one(post).inserted_id
print(post_id)