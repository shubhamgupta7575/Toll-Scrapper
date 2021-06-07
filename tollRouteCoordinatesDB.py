import mysql.connector
import csv
from datetime import datetime
import dbInfo
import sys
def tollRouteCoordinatesDB():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )
    vehicle_num = dbInfo.vehicle_num
    count = 0
    process_count = 0
    read_rows = 0
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor = db.cursor()
    csv_data = csv.reader(open('this_month.csv', newline=''))

    for row in csv_data:
        read_rows += 1
        if(read_rows>7):
            sql = "INSERT INTO route_report (dtm,vehicle_no, latitude, longitude, address, created_at) VALUES ('%s','%s','%s','%s','%s','%s');" % (row[1], vehicle_num, row[2], row[3], row[6], dt_string)
            try:
               # Execute the SQL command
               process_count += 1
               cursor.execute(sql)
               count += cursor.rowcount

               # Commit your changes in the database
               db.commit()
            except:
               # print("Error :",process_count, sys.exc_info()[0])
               # Rollback in case there is any error
               db.rollback()
    f = open("output.txt", "a")
    f.write(dt_string+"- Total Processed Data "+format(process_count)+" and Total "+format(count)+" GPS data inserted successfully!"+"\n")
    f.close()
    print("Total Processed Data {} and Total {} GPS data inserted successfully! ".format(process_count,count))

if __name__ == "__main__":
    tollRouteCoordinatesDB()
