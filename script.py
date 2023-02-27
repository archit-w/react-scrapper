from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
from io import StringIO
import time
import re
import csv
import random  

def clean_html(strings):
    if not strings:
        return "n/a"
    return  (re.sub('<[^<]+?>', '', str(strings)))

header = ['url', 'reservation number', 'payment method', 'amount','pickup location','model','details']
data_list = list()
#data_list.append(header)

DRIVER_PATH = './chromedriver'
the_file = open('links.csv')
#the_file = open('a.csv')

urls = the_file.readlines()
for url in urls: 
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(3)
    data = driver.page_source
    soup = bs4.BeautifulSoup(data, 'html.parser')
    reservation_number = soup.find_all("h5", class_ = "promocode-applied-box")
    payment_method = soup.find_all("h2",class_="text-16 font-bold")
   #Error Payment
    if(len(payment_method) == 0 ):
        print(url, "Error Payment")
        info_data = [url,' error processing',' error processing', 'error processing',' error processing',' error processing',' error processing',' error processing']
        data_list.append(info_data)
        filename = str(random.randint(0,999999999)) + ".csv"
    else:
        p_type = payment_method[0]
        if (len(payment_method) == 2):
            amount =  payment_method[1]
        else:
            amount = "n/a"
        reservation_number = (re.sub('<[^<]+?>', '', str(reservation_number[0])))
        p_type = clean_html(p_type)
        amount = clean_html(amount)

        info_data = list()
        location = soup.find_all("h3",class_="StationDetails__headline")
        location = str(re.sub('More Info', '', clean_html(location)))
        #pickup_location = location[0]
        #dropoff_location = location[1]
        dates = clean_html(soup.find_all("p",class_="StationDetails__subline"))
        driver_details = clean_html(soup.find_all("div",class_="custom-input-type-wrap"))
        car_type = clean_html(soup.find_all("h5",class_="font-bold mb-1"))
        tmp_data = list()
        tmp_data.append(url)
        tmp_data.append(reservation_number)
        tmp_data.append(p_type)
        tmp_data.append(amount)
        tmp_data.append(location)
        tmp_data.append(car_type)
        tmp_data.append(driver_details)

        print(tmp_data)
        data_list.append(tmp_data)
        
    driver.close()
the_file.close()
print(data_list)
with open(filename, 'w') as csvfile: 
  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)  
    for l in data_list:
        csvwriter.writerow(l) 


