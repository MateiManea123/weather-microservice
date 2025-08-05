import os
from concurrent import futures
import time
import grpc
import weather_pb2
import weather_pb2_grpc
from models.mongo_model import insert_city_doc
from weather_pb2_grpc import WeatherServiceServicer
import requests
from dotenv import load_dotenv, dotenv_values
load_dotenv()

class WeatherServiceServicer(weather_pb2_grpc.WeatherServiceServicer):

    def GetWeather(self, request_iterator, context):
        api_key = os.getenv("API_KEY")
        for request in request_iterator:
            print("GetWeather Request Made:")
            print(request)
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={request.city_name}&appid={api_key}&units=metric"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                weather_reply = weather_pb2.WeatherResponse()
                weather_reply.city_name = data["name"]
                weather_reply.temperature = data["main"]["temp"]
                weather_reply.description = data["weather"][0]["description"]
                weather_reply.humidity = data["main"]["humidity"]
                weather_reply.wind_speed = data["wind"]["speed"]
                insert_city_doc(weather_reply)
                yield weather_reply


            except requests.exceptions.HTTPError:
                yield weather_pb2.WeatherResponse(
                    city_name=request.city_name,
                    temperature=-1.0,
                    description="City not found or API error.",
                    humidity=0,
                    wind_speed=0.0
                )

            except requests.exceptions.RequestException as req_err:
                yield weather_pb2.WeatherResponse(
                    city_name=request.city_name,
                    temperature=-1.0,
                    description=f"Request failed: {req_err}",
                    humidity=0,
                    wind_speed=0.0
                )

            except KeyError as key_err:
                yield weather_pb2.WeatherResponse(
                    city_name=request.city_name,
                    temperature=-1.0,
                    description=f"Malformed response: {key_err}",
                    humidity=0,
                    wind_speed=0.0
                )

            except Exception as e:
                yield weather_pb2.WeatherResponse(
                    city_name=request.city_name,
                    temperature=-1.0,
                    description=f"Unexpected error: {e}",
                    humidity=0,
                    wind_speed=0.0
                )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()



