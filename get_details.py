from concurrent.futures import ThreadPoolExecutor
import csv
import random
import requests
import json
import time
from datetime import datetime
import os
import numpy as np

today = datetime.today().strftime('%Y-%m-%d')

username = 'massive'
password = 'connect123'

proxies = {
	"http": f'http://{username}:{password}@all.dc.smartproxy.com:10000',
	"https": f'http://{username}:{password}@all.dc.smartproxy.com:10000'
}

cat_ids = {}

def main():
	all_ad_ids = []
	a_r_t = []
	a_r_t2 = []
	categories = []
	categories2 = []

	# new_folder = str(today)
	# parent = 'images/image_files/'

	# path = os.path.join(parent,new_folder)

	# os.makedirs(path, exist_ok=True)
	# with open('access.json', 'r', encoding='utf-8') as f:
	#     tokens = json.load(f)
	#     for token in tokens['data']:
	#         refresh_token = token['details']['refresh_token']
	#         token = token['bearer']
	#         a_r_t.append({'token': token,'refresh_token':refresh_token})

	with open('categories.json', 'r', encoding='utf-8') as f:
		cats = json.load(f)
		cats = cats['data']['categories']
		for cat in cats:
			cat = cat['id']
			categories.append(cat)
	with open('new_cat_ids.json', 'r', encoding='utf-8') as f:
		cats = json.load(f)
		cats = cats['data']['categories']
		for cat in cats:
			cat = cat['id']
			categories2.append(cat)


	with open('access.csv', 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for r in reader:
			a_r_t.append({"token" :r['token'],"refresh_token":r['refresh_token']})

	with open('noaccount_access.csv', 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for r in reader:
			a_r_t2.append({"token" :r['token'],"refresh_token":r['refresh_token']})
	i = 0
	while True:
		cat_list = []
		if i == 0:
			get_list(40,0,400,a_r_t,categories,i)
			i = 1
		elif i == 1:
			get_list(40,0,400,a_r_t2,categories2,i)
			i = 0
		time.sleep(120)
		i = 0
	
with open('cat_ids.json', 'r', encoding='utf-8') as f:
		cat_ids = json.load(f)

def new_token(token, refresh_token):
	bearer = ''

	HEADERS = {
		'authorization': f'Bearer {token}',
		'Referer': 'm.olx.ro'
	}
	details = {
		"grant_type": "refresh_token",
		"refresh_token": f"{refresh_token}",
		"client_id": "100022",
		"client_secret": "hu76l0Wue78XZZrhbhuVJwmJmlAdn0Lts3ZI4Vdk3lgXkRnO"
	}

	try:
		a_token = requests.post('https://m.olx.ro/api/open/oauth/token/', data = details, headers=HEADERS, proxies=proxies)
		if a_token.status_code > 200:
			bearer = a_token.json()["error"]
			return False,bearer
		else:
			bearer = a_token.json()
			bearer = bearer['access_token']
			return bearer
	except Exception as error:
		return False,error


def download_image(link ,id):
	try:
		with open(f'images/image_files/{id}.jpeg', 'wb') as f:
			image = requests.get(link)
			f.write(image.content)
	except Exception as error:
		print(error)

def get_list_details(bearer, ad):
	try:
		bearer = str(bearer)
		HEADERS = {
			'authorization': f'Bearer {bearer}',
			'Referer': 'm.olx.ro'
		}
		phone_number = ''
		results = []
		image_links = []
		ad_link = ad['url']
		ad_id = ad['id']
		ad_id = str(ad_id)
		# print(ad_id)
		
		ad_title = ad['title']
		ad_title = str(ad_title).replace('<br />', '')

		price = ''
		cur = ''
		cat =''
		time.sleep(2)
		cat1 = ''
		cat2 = ''
		cat_id = 0
		with requests.Session() as s:
			cat = s.get(f'https://www.olx.ro/api/v1/targeting/data/?page=ad&params%5Bad_id%5D={ad_id}', proxies=proxies).json()
		
		try:
			cat1 = cat['data']['targeting']['cat_l0_name']
			cat2 = cat['data']['targeting']['cat_l2_name']
			cat_id = cat_ids['data'][cat1]
		except:
			cats = ['cat_l0_name','cat_l1_name']
			for c in cat_ids['data']:
				for cat_name in cats:
					if c == cat['data']['targeting'][cat_name]:
						cat1 = cat['data']['targeting'][cat_name]
						cat_id = cat_ids['data'][c]
						cat2 = cat['data']['targeting'][cat_name]
		try:
			price = cat['data']['targeting']['ad_price']
			cur = cat['data']['targeting']['currency']
		except:
			pass
		location = f"{ad['location']['city']['name']}"
		sub_location = f"{ad['location']['region']['name']}"
		username = ad['user']['name']

		desc = ad['description']
		desc = str(desc).replace(',', '3z@z3').replace('\n', '').replace('\r', '')

		time.sleep(random.randrange(0,5))
		phone = ''
		with requests.Session() as s:
			res = s.get(f'https://www.olx.ro/api/v1/offers/{ad_id}/limited-phones', 
							headers=HEADERS, proxies=proxies)
			phone = res.json()

		if res.status_code == 200:
			phone = phone['data']['phones']
			if len(phone) > 0:
				phone_number = phone[0]
			else:
				phone_number = f'No phone number {phone}'
				return [],False,phone_number
		else:
			if res.status_code > 200:
				phone_number = f'---: Error: {res.json()["error"]}'
			return [],False,phone_number
		seller_type = ''
		ad_type = ad['business']
		if ad_type is True:
			seller_type = 'Firma'
		elif ad_type is False:
			seller_type = 'Persoana fizica'

		features = ['Stare', 
					'Marca', 
					'Marca2',
					'Model', 
					'Caroserie', 
					'Culoare', 
					'An de fabricatie', 
					'Combustibil',
					'Putere', 
					'Capacitate motor', 
					'Numar de usi', 
					'Cutie de viteze', 
					'Rulaj', 
					'Serie sasiu (VIN)', 
					'Volan', 
					'Sarcina utila', 
					'Tara de origine', 
					'Compartimentare', 
					'Suprafata utila', 
					'An constructie', 
					'Etaj', 
					'Camere', 
					'Locuinta mobilata / utilata', 
					'Extravilan / intravilan']

		feat = ad['params']
		check = ''
		
		image_len = len(ad['photos'])
		image_link1 = 'None'
		image_link2 = 'None'
		if image_len > 1:
			image_link1 = str(f"{ad['photos'][0]['link']}").replace(';s={width}x{height}', '')
			image_link2 = str(f"{ad['photos'][1]['link']}").replace(';s={width}x{height}', '')
		elif image_len == 1:
			image_link1 = str(f"{ad['photos'][0]['link']},{ad['photos'][0]['link']}").replace(';s={width}x{height}', '')

		# results.append(ad_link)
		results.append(ad_id)
		results.append(ad_title)
		results.append(price)
		results.append(cur)
		results.append(cat_id)
		results.append(location)
		results.append(sub_location)
		results.append(username)
		results.append(phone_number)
		results.append(desc)
		results.append(seller_type)

		for f in features:
			f = f.lower()
			if f == 'marca' and cat1 == "Autoturisme":
				check  = cat2
				results.append(check)
				results.append('')
				continue

			elif f == 'camere' and ('camere' in cat2 or 'camera' in cat2):
				check = cat2[:1]
				results.append(check) 
				continue

			for fe in feat:
				name = fe['name']
				name = str(name).lower()

				if f == name:
					check = fe['value']['label']
					break

				elif (f == 'marca2' and name == 'marca') or (f == 'brand' and name == 'brand'):
					check = fe['value']['label']
					results[13] = check
					break

				else:
					check = ''

			re = ['cm³','CP','km','GB','m²']
			for tag in re:
				if tag in check:
					check = check.replace(tag,'').replace(' ', '')

			if f == 'marca2' or f == 'brand':
				continue

			elif f == 'marca':
				check = ''
				results.append(check)
				results.append(check)
				continue
			results.append(check)

		image_links.append(image_link1)
		image_links.append(image_link2)
		for i in image_links:
			if i == 'None':
				results.append('')
				continue
			image_id = str(i).split('/')[5].replace('-RO', '')
			new_image_link = f'MAMMAYA22MAMA/{image_id}.jpeg'
			results.append(new_image_link)

			time.sleep(2)
			download_image(i,image_id)
		
		results = [str(r).replace(',', '3z@z3').replace('\n', '').replace('\r', '') for r in results]
		return results,True,phone_number,{"id":ad_id}
	except Exception as error:
		return [],False,error

def get_data(proxy,limit,offset,cat_id,i):
	url = ''
	if i == 1:
		url1 = f'https://www.olx.ro/api/v1/offers/?offset={offset}&limit={limit}&category_id={cat_id}'
		url2 = f'https://www.olx.ro/api/v1/homescreen/?offset={offset}&limit={limit}&query=noi'
		# urls = [url1,url2]
		url = url1
		# url = random.choice(urls)
	
	elif i == 0:
		url1 = f'https://www.olx.ro/api/v1/homescreen/?offset={offset}&limit={limit}&query=noi'
		url2 = f'https://www.olx.ro/api/v1/offers/?offset={offset}&limit={limit}&category_id={cat_id}'
		url3 = f'https://www.olx.ro/api/v1/offers/?offset={offset}&limit={limit}&category_id=56'
		urls = [url1,url2,url3]
		url = random.choice(urls)
		


	data = []
	alt_data = []
	try:
		with requests.Session() as s:
			data = s.get(url,proxies=proxy).json()
		data = data['data']
		return data 
	except Exception as error:
		print(error)
		return False

def get_list(limit,offset,end,tokens,categories,c):
	print(f'Starting process')
	counter = 0
	state = 1
	while counter < round(len(tokens)/5):
		with open('images/wait_check.csv','r') as f:
			reader = csv.reader(f)
			for r in reader:
				state = int(r[0])
				
		if state == 1:
			time.sleep(1200)

		len_data = 0
		offset = 0

		both_tokens = [tokens[counter + counter],
						tokens[(counter + counter) + 1],
						tokens[(counter + counter) + 2],
						tokens[(counter + counter) + 3],
						tokens[(counter + counter) + 4] if (counter + counter) + 4 < len(tokens) else 'none']

		token_list = []

		count  = 200
		token_count = 5

		for token in both_tokens:
			if token == 'none':
				count -= 40
				token_count -= 1
				continue
			refresh_token = str(token['refresh_token']).strip()
			token = str(token['token']).strip()

			n_token = new_token(token,refresh_token)

			if not n_token[0]:
				print(f"---:No token because: {n_token[1]}")
				count -= 40
				token_count -= 1
				continue
			else:
				HEADERS = {
					'authorization': f'Bearer {n_token}',
					'Referer': 'm.olx.ro'
				}
				try:
					phone_test = ''
					with requests.Session() as s:
						phone_test = s.get(f'https://www.olx.ro/api/v1/offers/243165867/limited-phones', 
									headers=HEADERS, proxies=proxies)

					if phone_test.status_code > 200:
						print(f"Can't work with {n_token}{phone_test.text}")
						count -= 40
						token_count -= 1
						continue
					else:
						token_list.append(n_token)
				except:
					count -= 40
					token_count -= 1
					continue
		try:
			new_list = []
			old_list = []
			while len(new_list) < count:
				offsets = [offset, offset + 40, offset + 80, offset + 120, offset + 160,
					offset + 200, offset + 240, offset + 280, offset + 320, offset + 360]
				cat_ids = [random.choice(categories) for _ in range(len(offsets))]
				c_list = [c for _ in range(len(offsets))]
				limits = [limit for _ in range(len(offsets))]
				proxy = [proxies for _ in range(len(offsets))]
				data = []
				try:
					with ThreadPoolExecutor(len(offsets)) as executor:
						results = executor.map(get_data,proxy,limits,offsets,cat_ids,c_list)
						for result in results:
							data += [r for r in result]

					if not data:
						print('No data')
					for ad in data:
						if ad not in old_list:
							old_list.append(ad)
						else:
							print(f'Found {ad["id"]} in old list')
							
					with open('ids.json', 'r+', encoding='utf-8') as f:
						file_data = json.load(f)
						for ad in old_list:
							if len(new_list) < count:
								id = {"id":ad['id']}
								if id not in file_data['data']:
									new_list.append(ad)
									file_data['data'].append(id)
								else:
									print(f'Filtered: {id}')
							else:
								break
						f.seek(0)
						json.dump(file_data, f, ensure_ascii=False, indent=4)
				except:
					pass

				if offset > end:
					offset = 0   
				else:
					offset += 40
				time.sleep(2)

			len_data = len(new_list)
			print(len_data)
			t_list = []

			for i in range(token_count):
				for k in range(round(len_data/token_count)):
					t_list.append(token_list[i])

			
	
			with ThreadPoolExecutor(len_data) as executor:
				results = executor.map(get_list_details,t_list,new_list)
				with open('results/results.csv', 'a', encoding='utf-8',newline='') as file:
					for result in results:
						print(result[2])
						if result[1]:					
							writer = csv.writer(file)
							writer.writerow(result[0])
				
		except Exception as error:
			print(error)
		print(f'Done with token set {counter}')
		counter += 1
		time.sleep(2)


if __name__ == '__main__':
	main()