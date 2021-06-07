import mysql.connector
import csv
from datetime import datetime
import dbInfo

def tollListDB():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    process_count = 0
    inserted_count = 0
    cursor = db.cursor()
    csv_data = csv.reader(open('final_toll_list.csv', newline=''))

    for row in csv_data:
        process_count += 1
        sql = "INSERT INTO toll_list (toll_code,toll_name, latitude, longitude, issue, created_at) VALUES ('%s','%s','%s','%s','%s','%s');" % (row[0], row[1], row[2], row[3], row[4], dt_string)

        try:
           # Execute the SQL command
           cursor.execute(sql)
           inserted_count +=1
           # Commit your changes in the database
           db.commit()

        except:
           # print("Error")
           # Rollback in case there is any error
           db.rollback()
    f = open("output.txt", "a")
    f.write(dt_string+"- Total Processed Data "+format(process_count)+" and Total "+format(inserted_count)+" Toll List data inserted successfully!"+"\n")
    f.close()
    print("Total Processed Data {} and Total {} Toll List data inserted successfully! ".format(process_count,inserted_count))
if __name__ == "__main__":
    tollListDB()
