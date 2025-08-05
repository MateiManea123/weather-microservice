from http.client import responses

import weather_pb2
import weather_pb2_grpc
import time
import grpc


def get_client_stream_requests():
    while True:
        city_name = input("Please enter a city name (or nothing to stop chatting):")

        if city_name == "":
            break

        weather_request = weather_pb2.WeatherRequest(city_name = city_name)
        yield weather_request
        time.sleep(1)



def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = weather_pb2_grpc.WeatherServiceStub(channel)


        responses = stub.GetWeather(get_client_stream_requests())

        for response in responses:
            print("GetWeather Response Received:")
            print(response)

if __name__ == "__main__":
    run()