from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_python import get_driver_settings, smartproxy
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.common.exceptions import TimeoutException
import time
import csv
from csv import DictReader
import json

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('window-size=300,700')
# options.add_argument(r"--user-data-dir=C:\Users\ihunn\AppData\Local\Google\Chrome\User Data")
# options.add_argument(r'--profile-directory=Profile 3')
options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

accounts = []
count = 0

with open('accounts.csv', 'r', encoding='utf-8') as f:
	reader = csv.reader(f)
	for r in reader:
		r = str(r)
		r = r[2: len(r)-2].replace("'", '').split(',')
		email = r[0]
		password = r[1].strip()
		account = {'email':email, 'password':password}
		accounts.append(account)

def get_cookies(file):
	with open(file, encoding='utf-8-sig')as f:
		reader = DictReader(f)
		cookies = list(reader)
	return cookies

def get_token(base):
	PATH = "C:\Windows\chromedriver.exe"
	driver = webdriver.Chrome(PATH,options=options)
	action = ActionChains(driver)
	action.send_keys(Keys.CONTROL, Keys.SHIFT, "i")
	action.perform()
	
	time.sleep(2)
	driver.get('https://m.olx.ro')

	time.sleep(2)
	driver.delete_all_cookies()

	time.sleep(2)
	cookies = get_cookies('cookies.csv')
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.refresh()

	global count
	while count < 10*base:
		account = accounts[count]
		token = ''
		refresh_token = ''
		email = account['email']
		password = account['password']

		try:
			time.sleep(2)
			driver.get('https://m.olx.ro/myaccount/')

			try:
				time.sleep(2)
				ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/main/div[8]/ul/li[5]/button'))).click()

				time.sleep(2)
				ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/main/div[8]/ul/div/div/div[2]/div/button[2]'))).click()
				time.sleep(2)
				driver.get('https://m.olx.ro/myaccount/')
			except:
				pass
			time.sleep(2)
			login_email_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
			
			time.sleep(2)
			driver.execute_script("arguments[0].value = '';", login_email_box)
			
			time.sleep(2)
			login_email_box.send_keys(email)

			time.sleep(2)
			login_pass_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
			
			time.sleep(2)
			login_pass_box.send_keys(Keys.CONTROL, "a") 
			login_pass_box.send_keys(Keys.DELETE)

			time.sleep(2)
			login_pass_box.send_keys(password)
			
			time.sleep(2)
			ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div[1]/form/button'))).click()

			time.sleep(5)
			try:
				friction_error_msg = ui.WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'friction-error-message.fblock'))).text
				friction_error_msg_2 = ui.WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'errorbox.br3.margintop20.marginbott20.pding10'))).text
				if friction_error_msg:
					if str(friction_error_msg) == 'Wrong username or password':
						break
					time.sleep(10)
					count+=1
					continue
				elif friction_error_msg_2:
					if str(friction_error_msg_2) == 'Wrong username or password':
						break
					time.sleep(10)
					count+=1
					continue
			except:
				pass
			time.sleep(5)
			cookie = driver.get_cookies()

			for item in cookie:
				if item['name'] == 'access_token':
					token = item['value']

				if item['name'] == 'refresh_token':
					refresh_token = item['value']
			if token == '' and refresh_token == '':
				time.sleep(10)
				print('No token')
				count+=1
				break

			token_data = {  
				"bearer": f'{token}',
				"details":{
					"grant_type":"refresh_token",
					"refresh_token": f'{refresh_token}',
					"client_id": "100022",
					"client_secret": "hu76l0Wue78XZZrhbhuVJwmJmlAdn0Lts3ZI4Vdk3lgXkRnO"
				}
			}
			with open('access.json', 'r+', encoding='utf-8') as f:
				file_data = json.load(f)
				file_data['data'].append(token_data)
				f.seek(0)
				json.dump(file_data, f, ensure_ascii=False, indent=4)
			
			time.sleep(2)
			driver.get('https://m.olx.ro/api/v1/users/logout/')

			time.sleep(10)
			count+=1
		except TimeoutException as error:
			print(error)
	with open('count.txt', 'w') as c:
		c.write(str(count))
	# driver.delete_all_cookies()
	driver.close()
	driver.quit()

def get_non_signup_token(channel):
	token_data ={}
	token = ''
	refresh_token = ''
	PATH = "C:\Windows\chromedriver.exe"
	driver = webdriver.Chrome(PATH,options=options)
	action = ActionChains(driver)
	action.send_keys(Keys.CONTROL, Keys.SHIFT, "i")
	action.perform()
	
	try:
		time.sleep(2)
		driver.get('https://m.olx.ro')
		time.sleep(5)
		cookies = driver.get_cookies()
		try:
			for cookie in cookies:
				if cookie['name'] == 'a_access_token':
					token = cookie['value']
				if cookie['name'] == 'a_refresh_token':
						refresh_token = cookie['value']
		except:
			for cookie in cookies:
				if cookie['name'] == 'access_token':
					token = cookie['value']
				if cookie['name'] == 'refresh_token':
						refresh_token = cookie['value']
		token_data = {  
			"bearer": f'{token}',
			"details":{
				"grant_type":"refresh_token",
				"refresh_token": f'{refresh_token}',
				"client_id": "100022",
				"client_secret": "hu76l0Wue78XZZrhbhuVJwmJmlAdn0Lts3ZI4Vdk3lgXkRnO"
			}
		}
		time.sleep(5)
		driver.quit()
	except Exception as error:
		print(error)
		driver.quit()
		return token_data
	return token_data


for _ in range(100):
	tokens = []
	channels = [i for i in range(20)]
	with ThreadPoolExecutor(20) as executor:
		results = executor.map(get_non_signup_token,channels)
		for result in results:
			tokens.append(result)
	with open('access.json', 'r+', encoding='utf-8') as f:
		file_data = json.load(f)
		file_data['data'] += tokens
		f.seek(0)
		json.dump(file_data, f, ensure_ascii=False, indent=4)
	time.sleep(600)

# i = 1
# while True:
# 	if count > len(accounts):
# 		break
# 	get_token(i)
# 	time.sleep(120)
# 	i+=1

# counts = [0, 10]

# with ThreadPoolExecutor(2) as executor:
#     try:
#         for result in executor.map(get_token, counts):
#             print(result)
#     except Exception as error:
#         print(error)