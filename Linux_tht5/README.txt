MQTT-CHATTI

Kuvaus:
Projektin tavoitteena oli luoda Chatti, johonka saa yhteyden http:n kautta.
Python-logger ohjelma kuuntelee topicia chat/messages ja tallentaa viestit SQL:ään tauluun MESSAGES.
Subscribe näyttää viestit reaaliajassa.

Rakenne:

- Mosquitto: kuuntelee portissa 1884.
- MySQL: taulu messages rakenteella:
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(50),
    message TEXT,
    client_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

- Käyttäjä: mqtt_user (salasana määritelty MySQL:ssä).
- Topic: chat/messages.

Koodi:

Loggerin pääkohdat:
- Yhdistyy brokeriin client_id:llä mqtt_logger.
- Tilaa topicin chat/messages.
- Parsii JSON‑viestin (nickname, text, clientId).
- Tallentaa tiedot MySQL‑tauluun.
- Lokittaa onnistuneet tallennukset.

Testaus:

1. Loggerin käynnistys:
python mqtt_logger.py

2. Viestin lähetys:
mosquitto_pub -p 1884 -t chat/messages -m '{"nickname":"Testi1","text":"Hei maailma!","clientId":"test123"}'

3. Subscriber‑testi:
mosquitto_sub -p 1884 -t chat/messages

4. SQL-tarkistus:
SELECT * FROM messages;
 Viestin pitäisi näkyä taulussa.

Tulokset:
- Lokissa näkyy:
INFO - Tilattu: chat/messages
INFO - Tallennettu: [Testi1] Hei maailma!...

- SQL‑taulussa uusi rivi:
nickname | message     | client_id | created_at
Testi1   | Hei maailma!| test123   | 2025-12-02 11:53:59
