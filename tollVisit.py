import mysql.connector
import dbInfo
from datetime import datetime

def tollVisit():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )
    cursor = db.cursor(buffered=True)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    process_count = 0
    total_discrepancies = 0
    total_not_discrepancies = 0
    qry = "SELECT dtm, toll_name, vehicle_no, actual_price, date_add(dtm, interval -30 minute), date_add(dtm, interval 30 minute) FROM toll_visit where status='C'"
    cursor.execute(qry)
    result = cursor.fetchall()

    for x in result:
       process_count += 1
       dtm = x[0]
       vehicle_num = x[2]
       toll_name = x[1]
       act_price = float(x[3])
       dt_frm = x[4]
       dt_to = x[5]
       query = 'SELECT dtm, price, vehicle_no FROM fastag_report WHERE toll_name Like "%{}%" AND vehicle_no="{}" AND dtm BETWEEN "{}" AND "{}";'.format(toll_name, vehicle_num, dt_frm, dt_to)
       cursor.execute(query)
       result2 = cursor.fetchall()
       if(cursor.rowcount>0):
           for final_res in result2:
               lst = []
               lst.append(final_res)
               deduct_price = float(lst[0][1])
               difference = abs(act_price-deduct_price)
               cursor1 = db.cursor(buffered=True)
               if(abs(act_price-deduct_price)>0.0):
                   total_discrepancies +=1
                   update_qry = "UPDATE `toll_visit` SET `status` = 'Y', deduct_price='{}', difference='{}' WHERE toll_name='{}' AND vehicle_no='{}' AND dtm='{}';".format(deduct_price, difference, toll_name, vehicle_num, dtm)
                   cursor1.execute(update_qry)
                   db.commit()
               elif(abs(act_price-deduct_price)==0.0):
                   total_not_discrepancies +=1
                   update_qry = "UPDATE `toll_visit` SET `status` = 'N', deduct_price='{}', difference='{}' WHERE toll_name='{}' AND vehicle_no='{}' AND dtm='{}';".format(deduct_price, difference, toll_name, vehicle_num, dtm)
                   cursor1.execute(update_qry)
                   db.commit()

    f = open("output.txt", "a")
    f.write(dt_string+"- Total Process: "+ format(process_count)+ ",Total Found Discrepancies: "+ format(total_discrepancies)+",Total Not Found Discrepancies: "+ format(total_not_discrepancies)+"\n")
    f.close()
    print("Total Process: ", process_count, ",Total Found Discrepancies: ", total_discrepancies, ",Total Not Found Discrepancies: ", total_not_discrepancies)
if __name__  ==  "__main__":
    tollVisit()
