from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import mysql.connector
from datetime import datetime
import dbInfo
def routeScrapper():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    vehicle_num = "HR02AM4455"
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )

    cursor = db.cursor()

    chrome_path = "../toll_scrapper/driver/chromedriver.exe"
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    # urlName = "http://track.motocopgps.com/modern/#/reports/route"
    urlName = "http://track.motocopgps.com/modern/#/login"


    driver = webdriver.Chrome(chrome_path,desired_capabilities=capa)
    driver.get(urlName)
    try:
        userID = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/form/div[1]/div/input'))
        )
        userID.send_keys('jeev12')

        password = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/form/div[2]/div/input'))
        )
        password.send_keys('123456')

        login = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="root"]/main/div/form/div[3]/div/button').click())

    except TimeoutException:
        print("Loading...")

    try:
        routeLink = WebDriverWait(driver, 5).until(
            lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/ul[2]/div[1]/div/div').click())
    except TimeoutException:
        print("Loading...")

        selectDevice = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tags-outlinedhhh"]'))
        )
        selectDevice.send_keys(Keys.DOWN, Keys.DOWN, Keys.ENTER, Keys.TAB, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.ENTER, Keys.TAB, Keys.TAB, Keys.ENTER)
    time.sleep(10)
    try:
        mytable = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/table/tbody')
        for row in mytable.find_elements_by_css_selector('tr'):
                lst = []
                for cell in row.find_elements_by_tag_name('td'):
                    lst.append(cell.text)
                sql = "INSERT INTO route_report (dtm, vehicle_no, latitude, longitude, address, created_at) VALUES ('%s','%s', '%s', '%s', '%s', '%s');" % (lst[0],vehicle_num,lst[4],lst[5],lst[6],dt_string)
                print(sql)
                # Execute the SQL command
                # cursor.execute(sql)
               # Commit your changes in the database
               #  db.commit()
        f = open("output.txt", "a")
        f.write(dt_string+"- Route Coordinates Data Downloaded Successfully!"+"\n")
        f.close()
        print("Route Coordinates Data Downloaded Successfully!")
                # print ("DateTIme =",lst[0])
                # print ("Address =",lst[-1])
        # for row in mytable.find_elements_by_css_selector('tr'):
        #     data = [row.text]
        #     print(data)
        #     for cell in row.find_elements_by_tag_name('td'):
        #         print(cell.text)

            # print(row.text)
    except TimeoutException:
        # db.rollback()
        print("Loading...")

    driver.close()

    # qry = "SELECT address, MIN(latitude), longitude FROM route_report GROUP BY address"
    # # print(qry)
    # cursor.execute(qry)
    #
    # result = cursor.fetchall()
    # for x in result:
    #   latitude=float(x[1])
    #   longitude = float(x[2])
    #   # print(x)
    #   finalLat ="{:.3f}".format(latitude)
    #   finalLong ="{:.3f}".format(longitude)
    #   sql = 'SELECT DISTINCT toll_name FROM toll_list WHERE latitude Like "{}%" OR longitude LIKE "{}%" GROUP BY id;'.format(finalLat, finalLong)
    #   # print(sql)
    #
    #   try:
    #        # Execute the SQL command
    #        cursor.execute(sql)
    #        result1 = cursor.fetchall()
    #        # print(result1)
    #        for plazaName in result1:
    #            for plaza in plazaName:
    #                query = 'SELECT DISTINCT toll_name, car_jeep_van_price FROM toll_prices WHERE toll_name Like "%{}%" GROUP BY car_jeep_van_price;'.format(plaza)
    #                cursor.execute(query)
    #                result2 = cursor.fetchall()
    #                print("Toll Name- ",result2[0][0], ", Price- ", result2[0][1])
    #        # Commit your changes in the database
    #        db.commit()
    #   except:
    #        # print("Error")
    #        # Rollback in case there is any error
    #        db.rollback()
if __name__ == "__main__":
    routeScrapper()
