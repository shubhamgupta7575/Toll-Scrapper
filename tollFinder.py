import mysql.connector
import dbInfo
from datetime import datetime
import sys
def tollFinder():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )
    vehicle_num = dbInfo.vehicle_num
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    count = 0
    found_toll = 0
    inserted_toll = 0
    cursor = db.cursor(buffered=True)
    qry = "SELECT address, latitude, longitude, dtm, date_add(dtm, interval -15 minute), date_add(dtm, interval 15 minute) FROM route_report WHERE vehicle_no='{}' ORDER BY dtm;".format(vehicle_num)
    cursor.execute(qry)

    result = cursor.fetchall()
    for x in result:
      latitude=str(x[1])
      longitude = str(x[2])
      dtm = x[3]
      dtm_frm = x[4]
      dtm_to = x[5]
      finalLat =(latitude[0:5])
      finalLong =(longitude[0:5])
      sql = 'SELECT DISTINCT toll_name FROM toll_list WHERE latitude Like "{}%" AND longitude LIKE "{}%";'.format(finalLat, finalLong)

      try:
           # Execute the SQL command
           cursor.execute(sql)
           result1 = cursor.fetchall()
           count += cursor.rowcount
           found_toll += 1
           for plazaName in result1:
               plaza=result1[0][0]
               query = 'SELECT toll_name, car_jeep_van_price FROM toll_prices WHERE toll_name Like "%{}%" ;'.format(plaza)
               cursor.execute(query)
               result2 = cursor.fetchall()
               if (cursor.rowcount==0):
                   f = open("output.txt", "a")
                   f.write(dt_string+"- No Price Data for "+ plaza+",Date Time:"+ dtm+"\n")
                   f.close()
                   print("No Price Data for", plaza,",Date Time:", dtm)
               else:
                   c2 = db.cursor(buffered=True)
                   act_price = result2[0][1]
                   qry = "SELECT * FROM toll_visit WHERE toll_name='{}' AND vehicle_no='{}' AND dtm BETWEEN '{}' AND '{}';".format(plaza, vehicle_num, dtm_frm, dtm_to)
                   c2.execute(qry)
                   if(c2.rowcount<=0):
                       c3 = db.cursor(buffered=True)
                       toll_visit_query = "INSERT INTO toll_visit (dtm, toll_name, vehicle_no, actual_price, created_at ) VALUES ('%s', '%s', '%s', '%s', '%s');" %(dtm, plaza, vehicle_num, act_price, dt_string )
                       c3.execute(toll_visit_query)
                       inserted_toll += 1

                   f = open("output.txt", "a")
                   f.write(dt_string+"- Date- "+dtm+",Vehicle No- "+vehicle_num+",Toll Name-"+plaza+ ",Price- "+ act_price+"\n")
                   f.close()
                   print("Date- ",dtm,",Vehicle No- ",vehicle_num,",Toll Name-",plaza, ",Price- ", act_price)


            # Commit your changes in the database
           db.commit()

      except:
           f = open("output.txt", "a")
           f.write("Error:"+ sys.exc_info()[0]+"\n")
           f.close()
           print("Error", sys.exc_info()[0])
           # Rollback in case there is any error
           # db.rollback()

    if (count ==0 ):
        print("No Data Found!")
        f = open("output.txt", "a")
        f.write(dt_string+"- No Data Found in Toll Finder Script!"+"\n")
        f.close()

    f = open("output.txt", "a")
    f.write(dt_string+"- Toll Found: "+format(found_toll)+ ",Inserted Toll: "+format(inserted_toll)+"\n")
    f.close()
    print("Toll Found: ",found_toll, ",Inserted Toll: ", inserted_toll)

if __name__  ==  "__main__":
    tollFinder()
