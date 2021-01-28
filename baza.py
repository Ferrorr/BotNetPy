import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="cojimar5aBi"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE sieci")

mycursor.execute("CREATE TABLE Target (id INT AUTO_INCREMENT PRIMARY KEY, adres_ip VARCHAR(255))")
mycursor.execute("CREATE TABLE Hosts (id INT AUTO_INCREMENT PRIMARY KEY, adres_ip VARCHAR(255))")