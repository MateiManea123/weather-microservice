from pymongo import MongoClient




def init_database():
    connection_string = "mongodb://localhost:27017/"
    client = MongoClient(connection_string)
    db = client.cities_weather
    return db