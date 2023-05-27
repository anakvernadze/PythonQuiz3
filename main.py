import sqlite3
import requests
import json

key = '887aaff89bee4fd742287bfd4afa2483'
city = 'Tbilisi'
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}'
resp = requests.get(url)
result = resp.json()
print(result)
print(json.dumps(result, indent=4))

conn = sqlite3.connect('db_weather.sqlite3.sqlite3')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS w_table (
                date_time TEXT,
                max_temp FLOAT,
                min_temp FLOAT,
                weather TEXT
            )''')

for forecast in result['list']:
    max_temp = forecast['main']['temp_max']
    min_temp = forecast['main']['temp_min']
    weather = forecast['weather'][0]['description']
    date_time = forecast['dt_txt']
    cur.execute("INSERT INTO w_table(date_time, max_temp, min_temp, weather) VALUES (?, ?, ?, ?)",
                (date_time, max_temp, min_temp, weather))

conn.commit()
conn.close()
