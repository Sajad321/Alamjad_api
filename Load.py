import csv
import pymysql

mydb = pymysql.connect(host='localhost',
                       user='root',
                       passwd='',
                       db='mrsmart')
cursor = mydb.cursor()

with open('doctors.csv', "r", newline='', encoding="utf-8") as csvfile:
    csv_data = csv.reader(csvfile, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_data:
        print(row)
        # cursor.execute('INSERT INTO zone(zone)'
        #                'VALUES("%s")',
        #                row)
        cursor.execute('INSERT INTO doctor_pharmacies(doctor_id,pharmacy_id)'
                       'VALUES("%s", "%s")',
                       row)
# close the connection to the database.
mydb.commit()
cursor.close()
print("Done")
