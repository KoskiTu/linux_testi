import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


#Yhdistä tietokantaan
conn = mysql.connector.connect(
    host="localhost",
    user="KoskTu",
    password="PandajaMurmeli97@",
    database="weather_db"
)
cursor = conn.cursor()

#Hae viimeisen 7 päivän data
cursor.execute("""
    SELECT timestamp, temperature, humidity
    FROM weather
    WHERE timestamp >= NOW() - INTERVAL 7 DAY
    ORDER BY timestamp DESC
""")
rows = cursor.fetchall()
cursor.close()
conn.close()

#Muodosta DataFrame
df = pd.DataFrame(rows, columns=["Aikaleima", "Lämpötila (°C)", "Ilmankosteus (%)"])
df = df.sort_values("Aikaleima")
df["Aikaleima"] = pd.to_datetime(df["Aikaleima"])

#Käyttöliittymä
st.title("🌤️ Säädata Helsingistä")
nakyma = st.radio("Valitse näkymä:", ["Päiväkeskiarvo", "10 min tarkkuus", "Kaikki datapisteet"])

#Näytä valittu kaavio
if nakyma == "Päiväkeskiarvo":
    st.subheader("📅 Päiväkohtainen keskiarvo")
    daily_df = df.set_index("Aikaleima").resample("1D").mean().dropna().reset_index()
    st.line_chart(daily_df.set_index("Aikaleima")[["Lämpötila (°C)", "Ilmankosteus (%)"]])

elif nakyma == "10 min tarkkuus":
    st.subheader("⏱️ 10 minuutin välein")
    tenmin_df = df.set_index("Aikaleima").resample("10T").mean().dropna().reset_index()
    st.line_chart(tenmin_df.set_index("Aikaleima")[["Lämpötila (°C)", "Ilmankosteus (%)"]])

else:
    st.subheader("🔎 Kaikki datapisteet")
    st.line_chart(df.set_index("Aikaleima")[["Lämpötila (°C)", "Ilmankosteus (%)"]])
