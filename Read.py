import pymysql
import csv

cnx = pymysql.connect(user='root', database='mrsmart')
cursor = cnx.cursor()

sql = "SELECT `zone_id` FROM `doctor`"
csv_file_path = 'my_csv_file.csv'

try:
    cursor.execute(sql)
    result = list()

    # The row name is the first entry for each entity in the description tuple.
    column_names = list()
    for i in cursor.description:
        column_names.append(i[0])

    result.append(column_names)
    for row in cursor:
        result.append(row)
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in result:
            csvwriter.writerow(row)
    cursor.close()
except:
    print("Unable to fetch data!")

cnx.close()
