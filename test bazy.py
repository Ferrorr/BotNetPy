import mysql.connector

mydb = mysql.connector.connect(
  host="10.164.57.181",
  user="Szymon",
  password="cojimar5aBi",
  database="sieci"
)

mycursor = mydb.cursor()