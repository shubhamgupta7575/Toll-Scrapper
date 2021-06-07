import mysql.connector
import csv
from datetime import datetime
import dbInfo

def tollPriceDB():
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
    csv_data = csv.reader(open('dataset1.csv', newline=''))

    for row in csv_data:
        process_count += 1
        sql = "INSERT INTO toll_prices (toll_name, car_jeep_van_price, lcv_price, bus_truck_price, upto_three_axe_price, four_to_six_price, seven_price, fee_effective_date, hcm, revision_date) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' );" % (row[0].strip(), row[2].split(';')[0], row[3].split(';')[0], row[4].split(';')[0], row[5].split(';')[0], row[6].split(';')[0], row[8].split(';')[0], row[1], row[7].split(';')[0], row[9])
        try:
           # Execute the SQL command
           cursor.execute(sql)
           inserted_count += 1
           # Commit your changes in the database
           db.commit()
        except:
           # print("Error")
           # Rollback in case there is any error
           db.rollback()
    f = open("output.txt", "a")
    f.write(dt_string+"- Total Processed Data "+format(process_count)+" and Total "+format(inserted_count)+" Toll Price data inserted successfully!"+"\n")
    f.close()
    print("Total Processed Data {} and Total {} Toll Price data inserted successfully! ".format(process_count,inserted_count))
if __name__ == "__main__":
    tollPriceDB()
