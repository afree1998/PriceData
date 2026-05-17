import mysql.connector
import csv
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="priceInfo"
)
cursor = mydb.cursor()
df = pd.read_csv("payData.csv")

for _, row in df.iterrows():
    cursor.execute("Insert into info (name, price, date) Values(%s, %s, %s), 'Wage', row['CES0500000003'], row['observation_date']")
    mydb.commit()
    print(cursor.rowcount, "Record inserted.")

