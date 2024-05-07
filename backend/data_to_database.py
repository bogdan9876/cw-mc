import serial
import mysql.connector

db_connection = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="bogda765",
    database="health_data"
)
db_cursor = db_connection.cursor()

ser = serial.Serial('COM3', 9600)

try:
    while True:
        data = ser.readline().decode().strip()

        hb_data = data.split(":")[1].strip()

        print("Received data - Heart Rate:", hb_data)

        db_cursor.execute("INSERT INTO health_data (heart_rate) VALUES (%s)",
                          (hb_data,))
        db_connection.commit()

        print("Data inserted:", data)

except KeyboardInterrupt:
    ser.close()
    db_cursor.close()
    db_connection.close()
