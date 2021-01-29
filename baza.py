import mysql.connector


mydb = mysql.connector.connect(
    host="178.43.168.155",
    user="Szymon",
    password="haslo1234",
    database="sieci",
    #auth_plugin='caching_sha2_password'
)

mycursor = mydb.cursor()


# mycursor.execute("CREATE TABLE Target (id INT AUTO_INCREMENT PRIMARY KEY, adres_ip VARCHAR(255))")
# mycursor.execute("CREATE TABLE Hosts (id INT AUTO_INCREMENT PRIMARY KEY, adres_ip VARCHAR(255))")