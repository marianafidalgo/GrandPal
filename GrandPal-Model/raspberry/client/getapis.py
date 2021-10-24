import requests
import subprocess

def get_weather():
  # base URL
  BASE_URL = "https://api.openweathermap.org/data/2.5/weather?units=imperial&"
  # City Name
  CITY = "Lisbon"
  # API key
  API_KEY = "1f8e15bf31ccf3205289bb512745f1ea"
  # upadting the URL
  URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
  # HTTP request
  response = requests.get(URL)
  # checking the status code of the request
  if response.status_code == 200:
    # getting data in the json format
    data = response.json()
    # getting the main dict block
    main = data['main']
    # getting temperature
    temperature = main['temp']
    temperature = (temperature - 32) * 5.0/9.0
    # getting the humidity
    humidity = main['humidity']
    # getting the pressure
    pressure = main['pressure']
    # weather report
    report = data['weather']
    print(f"{CITY:-^30}")
    print(f"Temperature: {temperature}")
    print(f"Humidity: {humidity}")
    print(f"Pressure: {pressure}")
    print(f"Weather Report: {report[0]['description']}")
    return "Hoje em lisboa temos " +str("{:.0f}".format(temperature)) + "graus celsius"
  else:
    # showing the error message
    print("Error in the HTTP request")

def play_radio():
  music_stream_uri = 'http://mcrscast1.mcr.iol.pt/comercial.mp3'
  subprocess.call('mpg123 http://mcrscast1.mcr.iol.pt/comercial.mp3', shell=True) #INSTALLL THIS
  exit(0)
