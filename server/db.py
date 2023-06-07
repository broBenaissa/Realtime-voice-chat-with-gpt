
from pymongo import MongoClient

client = MongoClient('mongodb+srv://benaissa:benaissamongodb@youssefcluster.ogkngyi.mongodb.net/') 
db = client['audio_chat_gpt']
collection = db['Historic']



  
