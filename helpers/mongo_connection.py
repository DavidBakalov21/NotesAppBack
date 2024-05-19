from pymongo import MongoClient
import certifi
def get_mongo_collection():
    client = MongoClient('mongodb+srv://davidbakalov33:JiU6uQHAvbh3b7orhrsth576rd665yg@cluster0.g73wh8t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', tlsCAFile=certifi.where())
    db = client['TestTask']
    return db
