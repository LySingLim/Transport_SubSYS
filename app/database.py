from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["TestDB"]  # Change database name as needed

# Define multiple collections
booking_collection = db["booking"]
users_collection = db["users"]
prices_collection = db["price"]