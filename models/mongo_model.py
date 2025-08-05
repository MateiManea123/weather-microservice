from services.db_intialiser import init_database
from datetime import datetime as dt
db = init_database()

def insert_city_doc(data):
    name = data.city_name
    city = db[name]
    new_city = {
        "city_name" : data.city_name,
        "temperature" : data.temperature,
        "description" : data.description,
        "humidity" : data.humidity,
        "wind_speed" : data.wind_speed,
        "time_added" : dt.now()
    }
    city.insert_one(new_city)

