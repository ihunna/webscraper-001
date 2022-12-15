from tabnanny import check
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
from selenium.common.exceptions import TimeoutException
import time
import requests
import csv
from bs4 import BeautifulSoup as bs
from csv import DictReader
import json
import random
import imaplib, email




options = Options()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--start-maximized') 
options.add_argument(r"--user-data-dir=C:\Users\ihunn\AppData\Local\Google\Chrome\User Data")
options.add_argument(r'--profile-directory=Profile 3')
options.add_argument('disable-infobars')
# options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
# options.add_argument("--disable-extensions")
set_device_metrics_override = dict({
				  "width": 390,
				  "height": 844,
				  "deviceScaleFactor": 50,
				  "mobile": True,
				  "screenWidth": 390, 
				#   "screenHeight": 844
			  })


def get_email_from_outlook(access_email, password):
	code = ''
	user = access_email
	password = password
	imap_url = 'imap-mail.outlook.com'
	imap = imaplib.IMAP4_SSL(imap_url,993)
	imap.login(user, password)
	imap.select("inbox")

	resp, items = imap.search(None,'TO',f'{access_email}', 'FROM', f'noreply@olx.ro')

	for n, num in enumerate(items[0].split(), 1):
		resp, data = imap.fetch(num, '(RFC822)')

		body = data[0][1].decode('utf-8')
		msg = str(email.message_from_string(body))
		try:
			start_link = msg.find('Pentru a-l activa')
			end_link = msg.find('De asemenea')
			code = msg[start_link:end_link]
			code = int(code.split(':')[1].strip())
		except:
			start_link = msg.find('Activeaza-ti contul: ')
			end_link = msg.find('email_link')
			code = msg[start_link:end_link + 10]
			code = code.split(':')[2].strip()
			code = f'https:{code}'
		return code

def get_cookies(file):
	with open(file, encoding='utf-8-sig')as f:
		reader = DictReader(f)
		cookies = list(reader)
	return cookies

def register(password):
	count = 0
	PATH = "C:\Windows\chromedriver.exe"
	driver = webdriver.Chrome(PATH,options=options)
	action = ActionChains(driver)

	# driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', set_device_metrics_override)

	# action.send_keys(Keys.CONTROL, Keys.SHIFT, "i")
	# action.perform()
	
	time.sleep(2)
	driver.get('https://www.olx.ro')

	time.sleep(2)
	driver.delete_all_cookies()

	time.sleep(2)
	cookies = get_cookies('cookies.csv')
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.refresh()

	time.sleep(5)
	with open('names.csv', 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for r in reader:
			check = 0
			time.sleep(2)
			token = ''
			refresh_token = ''
			if count == 10:
				break
			r = str(r)
			r = r[2: len(r)-2].replace("'", '').split(',')
			email = r[0]
			e_pass = r[1]
			receiving_address = email
			
			try:
				time.sleep(5)
				driver.get('https://www.olx.ro/cont/?ref%5B0%5D%5Baction%5D=myaccount&ref%5B0%5D%5Bmethod%5D=index')
				
				try:
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/main/div[1]/div[1]/div/button[2]'))).click()
					check = 1
				except:
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'register_tab'))).click()
					check = 0
				time.sleep(2)
				driver.execute_script("window.scrollTo(0,300)")

				email_box = ''
				pass_box = ''

				if check == 0:
					time.sleep(2)
					email_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userEmailRegister')))
					time.sleep(2)
					pass_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userPassRegister')))

				elif check == 1:
					time.sleep(2)
					email_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
					
					time.sleep(2)
					pass_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
				
				time.sleep(2)
				driver.execute_script("arguments[0].value = '';", email_box)

				time.sleep(2)
				email_box.send_keys(receiving_address)
				
				time.sleep(2)
				pass_box.send_keys(Keys.CONTROL, "a") 
				pass_box.send_keys(Keys.DELETE)

				time.sleep(2)
				pass_box.send_keys(password)
				
				if check == 0:
					time.sleep(2)
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'button_register'))).click()
				elif check == 1:
					time.sleep(2)
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/main/div[1]/div[2]/div/div/div[5]/form/button'))).click()
				
				time.sleep(2)
				driver.execute_script("window.scrollTo(300,400)")

				time.sleep(2)
				try:
					friction_error_msg = ui.WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'friction-error-message.fblock')))
					if friction_error_msg:
						time.sleep(60)
						continue
				except:
					pass
				
				if check == 0:
					time.sleep(7)
					ui.WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[2]/section/div[3]/div/ul/li[2]/form/div[5]/div/div/div/iframe')))
																											
					time.sleep(2)
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'recaptcha-anchor'))).click()
				
				elif check == 1:
					time.sleep(7)
					ui.WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[2]/div/div/div/div/main/div[1]/div[2]/div/div/div[5]/form/div[3]/div/div/div/div/iframe')))
																											
					time.sleep(2)
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'recaptcha-anchor'))).click()
				

				time.sleep(10)
				driver.switch_to.default_content()
				
				time.sleep(5)
				try:
					error_msg = ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'errorbox.br3.margintop20.marginbott20.pding10')))
					if error_msg:
						continue
				except:
					pass
				time.sleep(20)
				v_code = get_email_from_outlook(email, e_pass)
				print(f'---: Verification code: {v_code}')
				if not v_code:
					with open('not_verified_accounts.csv', 'a', encoding='utf-8') as file:
						file.write(f'{email}, {e_pass},')
						file.write('\n')
					continue
				
				if isinstance(v_code,int):
					i_token = ''
					i_refresh_token = ''
					time.sleep(5)
					ui.WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/main/div/a'))).click()
					
					
					time.sleep(2)
					ui.WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/main/div/form/div/div/input'))).send_keys(v_code)
					

					time.sleep(2)
					ui.WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/main/div/form/button[2]'))).click()
					
					with open('accounts.csv', 'a', encoding='utf-8') as file:
						file.write(f'{email}, {e_pass},')
						file.write('\n')

					time.sleep(5)
					options2 = Options()

					options2.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
					options2.add_argument('window-size=500,700')

					PATH = "C:\Windows\chromedriver.exe"
					driver2 = webdriver.Chrome(PATH,options=options2)

					time.sleep(5)
					driver2.get('https://m.olx.ro/myaccount/')
					
					time.sleep(2)
					cookies = get_cookies('cookies.csv')
					for cookie in cookies:
						driver2.add_cookie(cookie)
					driver2.refresh()

					try:
						time.sleep(2)
						ui.WebDriverWait(driver2,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/main/div[8]/ul/li[5]/button'))).click()

						time.sleep(2)
						ui.WebDriverWait(driver2,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/main/div[8]/ul/div/div/div[2]/div/button[2]'))).click()
						time.sleep(2)
						driver2.get('https://m.olx.ro/myaccount/')
					except:
						pass
					time.sleep(2)
					login_email_box = ui.WebDriverWait(driver2, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
					
					time.sleep(2)
					driver2.execute_script("arguments[0].value = '';", login_email_box)
					
					time.sleep(2)
					login_email_box.send_keys(email)

					time.sleep(2)
					login_pass_box = ui.WebDriverWait(driver2, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
					
					time.sleep(2)
					login_pass_box.send_keys(Keys.CONTROL, "a") 
					login_pass_box.send_keys(Keys.DELETE)

					time.sleep(2)
					login_pass_box.send_keys(password)
					
					time.sleep(2)
					ui.WebDriverWait(driver2, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/main/div[2]/div[2]/div[1]/form/button'))).click()

					time.sleep(10)
					cookie = driver2.get_cookies()
					
					for item in cookie:
						if item['name'] == 'access_token':
							i_token = item['value']

						if item['name'] == 'refresh_token':
							i_refresh_token = item['value']
					if i_token == '' and i_refresh_token == '':
						time.sleep(10)
						print('No token')
						count+=1
						break

					token_data = {  
						"bearer": f'{i_token}',
						"details":{
							"grant_type":"refresh_token",
							"refresh_token": f'{i_refresh_token}',
							"client_id": "100022",
							"client_secret": "hu76l0Wue78XZZrhbhuVJwmJmlAdn0Lts3ZI4Vdk3lgXkRnO"
						}
					}
					with open('access.json', 'r+', encoding='utf-8') as f:
						file_data = json.load(f)
						file_data['data'].append(token_data)
						f.seek(0)
						json.dump(file_data, f, ensure_ascii=False, indent=4)

					time.sleep(5)
					driver2.delete_all_cookies()
					driver2.close()
					driver2.quit()
					
				else:
					driver.get(v_code)

					time.sleep(3)
					driver.get('https://m.olx.ro/myaccount/?backUrl=%2Fcont%2Fmenu%2F%3Fsource%3Dmy_olx')

					time.sleep(2)
					login_email_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userEmail')))
					
					time.sleep(2)
					driver.execute_script("arguments[0].value = '';", login_email_box)
					
					time.sleep(2)
					login_email_box.send_keys(email)

					time.sleep(2)
					login_pass_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userPass')))
					
					time.sleep(2)
					driver.execute_script("arguments[0].value = '';", login_pass_box)

					time.sleep(2)
					login_pass_box.send_keys(password)
					
					time.sleep(2)
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'se_userLogin'))).click()

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
				
				
					with open('accounts.csv', 'a', encoding='utf-8') as file:
						file.write(f'{receiving_address}, {password},')
						file.write('\n')

					time.sleep(5)
					cookie = driver.get_cookies()
				
					with open('cookies.json','w', encoding='utf-8') as f:
						json.dump(cookie,f,ensure_ascii=False, indent=4)

					for item in cookie:
						if item['name'] == 'access_token':
								token = item['value']

						if item['name'] == 'refresh_token':
							refresh_token = item['value']

					if token == '' and refresh_token == '':
						time.sleep(2)
						print('No token')
						count+=1

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
				
			except TimeoutException:
				print('---: Element not found!')
				exit()
			count +=1
			time.sleep(20)
			# driver.delete_all_cookies()
			# driver.refresh()
	driver.close()
	driver.quit()

		


def verify(password):
	PATH = "C:\Windows\chromedriver.exe"
	driver = webdriver.Chrome(PATH,options=options)

	time.sleep(2)
	driver.get('https://www.olx.ro')

	time.sleep(2)
	# cookies = get_cookies('cookies.csv')
	# for cookie in cookies:
	# 	driver.add_cookie(cookie)
	# driver.refresh()

	try:
		ui.WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
	except:
		pass

	with open('not_verified_accounts.csv', 'r', encoding='utf-8') as f:
				reader = csv.reader(f)
				for r in reader:
					time.sleep(5)
					driver.get('https://www.olx.ro/cont/logout/')

					r = str(r)
					r = r[2: len(r)-2].replace("'", '').split(',')
					email = r[0]
					e_pass = r[1]
					receiving_address = email
					time.sleep(5)
					v_code = get_email_from_outlook(email, e_pass)
					print(f'---: Verification link: {v_code}')
					if not v_code:
						continue
					time.sleep(5)
					driver.get(v_code)

					time.sleep(5)
					driver.get('https://www.olx.ro/myaccount/')

					time.sleep(2)
					login_email_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userEmail')))
					
					time.sleep(2)
					driver.execute_script("arguments[0].value = '';", login_email_box)
					
					time.sleep(2)
					login_email_box.send_keys(receiving_address)

					time.sleep(2)
					login_pass_box = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userPass')))
					
					time.sleep(2)
					driver.execute_script("arguments[0].value = '';", login_pass_box)

					time.sleep(2)
					login_pass_box.send_keys(password)
					
					time.sleep(2)
					ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'se_userLogin'))).click()
					
					# time.sleep(5)
					# ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[1]/a')))
					
					cookie = driver.get_cookies()

					for item in cookie:
						if item['name'] == 'access_token':
							token = item['value']

						if item['name'] == 'refresh_token':
							refresh_token = item['value']
					if token == '' and refresh_token == '':
						time.sleep(2)
						print('No token')
						count+=1

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
						with open('accounts.csv', 'a', encoding='utf-8') as file:
							file.write(f'{receiving_address}, {password},')
							file.write('\n')

register('Massive123$$$')