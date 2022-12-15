from concurrent.futures import ThreadPoolExecutor
import csv
from selenium_python import get_driver_settings, smartproxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
import time, random
import json
from bs4 import BeautifulSoup as bs
import requests


options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized') 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")


username = 'massive123'
password = 'ekedende'

url = 'https://www.olx.ro/d/oferta/opel-astra-g-1-6-benzina-2001-IDfWJBa.html'

proxy = f'http://{username}:{password}@ro.smartproxy.com:13001'
  

features = ['Stare','Model','Caroserie','Culoare','An de fabricatie','Combustibil','Putere','Capacitate motor','Numar de usi','Cutie de viteze','Rulaj','Volan','Compartimentare','Suprafata utila','An constructie','Etaj','Extravilan / intravilan','Capacitate']



def search(count):
    links = []
    # while timer > 0:
    with open('links.csv', 'r') as f:
        reader = csv.reader(f)
        for r in reader:
            r = str(r)
            links.append(r[2: -6])
        # links = []
        # link = requests.get(f'https://m.olx.ro/api/v1/homescreen/?offset={offset}&limit={limit}',proxies={'http': proxy, 'https': proxy}).json()
        # link = link['data']
        # for l in link:
        #     l = l['url']
        #     links.append(l)
        # time.sleep(5)
        PATH = "C:\Windows\chromedriver.exe"
        driver = webdriver.Chrome(PATH,desired_capabilities=smartproxy(),options=options)
        try:
            counter = 0
            while counter < 100:
                results = []
                url = links[count + counter]
                results.append(url)
                try:
                    driver.get(url)
        
                    time.sleep(2)
                    try:
                        ui.WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
                    except:
                        pass
                    time.sleep(2)
                    details_div = ''
                    try:
                        details_div = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[1]/div[2]')))
                    except:
                        details_div = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[1]/div[2]')))
                    
                    title = details_div.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[1]/div[2]/div[2]').text
                    title = str(title).replace(',', '')
                    print(title)
                    price = details_div.find_element(By.CLASS_NAME, 'css-okktvh-Text.eu5v0x0').text
                    price = str(price)
                    # print(f'---Price: {price}')
                    cur = ''
                    if 'lei' in price:
                        cur = 'lei'
                        price.replace('lei', '')
                        
                    else:
                        cur = '€'
                        price.replace('€', '')
                    cat_div = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[2]/div[1]/ol')
                    all_cat = cat_div.find_elements(By.TAG_NAME, 'li')
                    cat_ = all_cat[1].text
                    cat_ = str(cat_).replace(',', '')
                    sub_cat = all_cat[2].text
                    # print(f'---:Category: {cat_}')
                    # print(f'---:Subcategory: {sub_cat}')

                    location_div = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[2]/div[2]/div/section/div[1]/div')
                    all_p = location_div.find_elements(By.TAG_NAME, 'p')
                    p_1 = all_p[0].text
                    p_1 = str(p_1).replace(',', '')
                    p_2 = all_p[1].text
                    # print(f'---:Location: {all_p[0].text} {all_p[1].text}')

                    user_box = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[2]/div[1]')
                    time.sleep(2)
                    driver.execute_script("arguments[0].scrollIntoView(true);",user_box)
                    user_name = user_box.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[2]/div[1]/section/a/div/div[2]/h2').text
                    # print(f'---User: {user_name}')

                    call_btn = user_box.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[2]/div[1]/div[2]/button[1]')

                    time.sleep(5)
                    call_btn.click()

                    phone_number = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[2]/div[1]/div[2]/button[1]/span/a'))).text
                    phone_number = str(phone_number ).replace(',', '').replace("'", '')
                    phone_number = phone_number[0:12]
                    # print(f'---:Phone: {phone_number }')

                    description = driver.find_element(By.CLASS_NAME, 'css-g5mtbi-Text')
                    descript = description.text
                    descript = str(descript)
                    descript = descript.replace(',', '').replace('\n', ' ').replace('\r', '')
                    # print(f'---Description: {descript}')

                    details = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[1]/div[2]/ul')
                    all_details = details.find_elements(By.TAG_NAME, 'li')
                    f_detail = all_details[0].text
                    # print(f'Details:{f_detail}')
                    details_list = []

                    selected = ''
                    all_i = ''
                    for f in features:
                        for all in all_details:
                            all_i = all.text
                            all_i = str(all_i)
                            if ':' not in all_i:
                                continue
                            side_1 = all_i.split(':')
                            # print(f'---:All: {all_i}')
                            # print(f'---:Tester: {f}:{side_1[1]}')
                            if all_i == f'{f}:{side_1[1]}':
                                select= all_i.split(':')
                                selected = select[1]
                                break
                            else:
                                selected = 'None'
                        details_list.append(selected)
                        # print(f'---Details second: {f} : {selected}')

                    img_con = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div/div[1]')
                    imgs_div = img_con.find_elements(By.TAG_NAME, 'img')
                    img_list = []
                    i = 0
                    for img in imgs_div:
                        if i == 2:
                            break
                        img_link =  img.get_attribute("src")
                        img_list.append(img_link)
                        # print(f'---: Image-Link: {img_link}')
                        i += 1

                    time.sleep(2)
                    id_div = driver.find_element(By.CLASS_NAME, 'css-1ferwkx')
                    driver.execute_script("arguments[0].scrollIntoView(true);",id_div)

                    time.sleep(2)
                    try:   
                        id_text = id_div.find_element(By.CLASS_NAME, 'css-9xy3gn-Text.eu5v0x0').text
                        id_text = str(id_text).split()
                        
                        print(f'ID: {id_text[1]}')
                    except:
                        id_text = id_div.find_element(By.CLASS_NAME, 'css-9xy3gn-Text.eu5v0x0').text
                        id_text = str(id_text).split()
                        # print(f'ID: {id_text[1]}')

                    results.append(id_text[1])
                    results.append(title)
                    results.append(price)
                    results.append(cur)
                    results.append(cat_)
                    results.append(sub_cat)
                    results.append(p_1)
                    results.append(p_2)
                    results.append(user_name)
                    results.append(phone_number )
                    results.append(descript)
                    results.append(f_detail)
                    for d in details_list:
                        results.append(d)
                    for i in img_list:
                        results.append(i)

                    with open('results.csv', 'a', encoding='utf-8') as f:
                        for result in results:
                            result = str(result).replace(',', '')
                            f.write(result)
                            f.write(',')
                        f.write('\n') 
                    print(f'---: Done with {count+1}')   
                except Exception as error:
                    print(error)
                count +=1
        except Exception as error:
            print(error)
            driver.delete_all_cookies()   
            driver.quit()
        # offset = limit
        # timer -=1

         
counts = [0, 100, 200, 300, 400, 500, 600, 700,800,900]
with ThreadPoolExecutor(10) as executor:
    try:
        for result in executor.map(search, counts):
            print(result)
    except Exception as error:
        print(error)
