from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import mysql.connector
import dbInfo


def tollScrapper():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )

    cursor = db.cursor()
    process_count = 0
    inserted_count = 0
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    chrome_path = "../toll_scrapper/driver/chromedriver.exe"
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    urlName = "https://fastaglogin.icicibank.com/CUSTLOGIN/Default.aspx?ReturnUrl=%2fCUSTLOGIN"
    driver = webdriver.Chrome(chrome_path,desired_capabilities=capa)
    driver.get(urlName)

    try:
        download_link = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="rdIndividualLogin"]')).click()

    except TimeoutException:

        print("Loading take too much time on step 1")


    try:
        download_link = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="chkLoginviaUsername"]')).click()
    except TimeoutException:
        print("Loading take too much time on step 2")

    try:
        userID = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtUserId"))
        )

        driver.execute_script("document.getElementById('txtUserId').value='talk2sk'")
        driver.execute_script("document.getElementById('txtPassword').value='Fastag@7543'")
        login = WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath('//*[@id="btnLogin"]').click())

    except TimeoutException:
        print("Loading take too much time on step 3")

    try:
        link = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="hyplnkView"]').click())
    except TimeoutException:
        print("Loading take too much time on step 4")

    try:
        mytable = driver.find_element_by_xpath('//*[@id="tripsblock"]/div[2]/table')
        for row in mytable.find_elements_by_css_selector('tr'):
                lst = []
                for cell in row.find_elements_by_tag_name('td'):
                    lst.append(cell.text)
                if lst:
                    process_count += 1
                    # print (lst)
                    dtm = lst[0]
                    yy = (dtm[6:10])
                    mm = (dtm[3:5])
                    dd = (dtm[0:2])
                    time_string = (dtm[11:])
                    dt = yy+"-"+mm+"-"+dd+" "+time_string
                    price = lst[5]
                    toll_name = lst[2]
                    vehicle_no = lst[4]
                    tag_no = lst[3]
                    # print("Date- ",dt)
                    sql = "INSERT INTO fastag_report (dtm, price, toll_name, vehicle_no, tag_no, created_at) VALUES ('%s','%s','%s','%s','%s', '%s' );" % (dt, price, toll_name, vehicle_no, tag_no, dt_string)
                    # print(sql)
                    try:
                      cursor.execute(sql)
                      inserted_count += 1
                      # # Commit your changes in the database
                      db.commit()
                    except mysql.connector.IntegrityError as err:
                        print("Error: {}".format(err))
                    # Execute the SQL command
                    # cursor.execute(sql)

        f = open("output.txt", "a")
        f.write(dt_string+"- Data Processed Count: "+str(process_count)+" ,Total Inserted Count: "+str(inserted_count)+"\n")
        f.close()
        print("Data Processed Count: ",process_count," ,Total Inserted Count: ",inserted_count)
    except TimeoutException:
        print("Loading take too much time on step 5")
    driver.close()

if __name__  ==  "__main__":
    tollScrapper()
