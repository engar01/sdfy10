import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

def get_weather_data():
    url = 'https://weather.com/uk-UA/weather/today/l/d5a591c0fea07a88bafe951d05212c82c562b62777e06492bf0a9d0598e7a180'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    temp = soup.find('span', {'data-testid': 'TemperatureValue', 'class': 'CurrentConditions--tempValue--MHmYY'}).text

    return float(temp[:-1])

def insert_data_to_db(temp):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather
                    (date text, time text, temperature real)''')
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")
    cursor.execute("INSERT INTO weather VALUES (?, ?, ?)", (date, time, temp))
    conn.commit()
    conn.close()

def main():
    temp = get_weather_data()
    insert_data_to_db(temp)
    print(f"Temperature: {temp}°C")

if __name__ == '__main__':
    main()