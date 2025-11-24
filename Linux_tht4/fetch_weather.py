import requests, mysql.connector, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Helsinki"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

# Debug: tulosta koko vastaus
print("API-vastaus:", data)

# Tarkista, että vastaus sisältää säädatan
if response.status_code != 200 or "main" not in data:
    print("Virhe API-kutsussa:", data.get("message", "Tuntematon virhe"))
    exit()


temp = data["main"]["temp"]
humidity = data["main"]["humidity"]
timestamp = datetime.now()

conn = mysql.connector.connect(
    host="localhost",
    user="KoskTu",
    password="PandajaMurmeli97@",
    database="weather_db"
)
cursor = conn.cursor()

# Luo taulu tarvittaessa
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    humidity INT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    humidity INT
)
""")
cursor.execute("INSERT INTO weather (timestamp, temperature, humidity) VALUES (%s, %s, %s)",
               (timestamp, temp, humidity))
conn.commit()
cursor.close()
conn.close()
