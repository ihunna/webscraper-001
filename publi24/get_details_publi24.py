from bs4 import BeautifulSoup as bs
import requests
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor
import random

username = 'massive'
password = 'connect123'

proxies = {
	"http": f'http://{username}:{password}@all.dc.smartproxy.com:10000',
	"https": f'http://{username}:{password}@all.dc.smartproxy.com:10000'
}


cat_ids = {}
with open('cat_ids_publi24.json', 'r', encoding='utf-8') as f:
	cat_ids = json.load(f)

def main(page):
	while page < 100:
		get_links(page)
		page += 1

def download_image(link ,id):
	try:
		with open(f'../images/image_files/{id}.jpeg', 'wb') as f:
			image = requests.get(link)
			f.write(image.content)
	except Exception as error:
		print(error)

def get_list_details(ad):
	try:
		time.sleep(random.randrange(2,4))
		link = ad['link']
		id = ad['id']['id']
		phone_number = ad['phone']
		seller_type = ad['ad_type']
		image_len = 0
		if seller_type == 'false':
			seller_type = 'Persoana fizica'
		else:
			seller_type = 'Firma'
		results = []
		specifications = []
		image_links = []
		cat_id = ''
		city = ''
		region = ''
		price = ''
		currency = ''
		username = ''
		image_link1 = 'none'
		image_link2 = 'none'
		HEADERS = {
			'authority': 'www.publi24.ro',
			'method': 'GET',
			'path': '/anunturi/imobiliare/de-vanzare/apartamente/apartamente-2-camere/anunt/apartament-2-camere-damaroaia-cu-vedere-la-lac/h676e85fd61i77egefd39i53h623g179.html',
			'scheme': 'https',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'accept-encoding':'gzip, deflate, br',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
			'cache-control': 'max-age=0',
			'referer': 'https://www.publi24.ro/anunturi/?pag=2',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
		}

		features = ['Stare', 
					'Marca', 
					'Marca2', 
					'Model', 
					'Categoria', 
					'Culoare', 
					'Data fabricatiei', 
					'Motorizare', 
					'Putere maxima', 
					'Capacitate cilindrica', 
					'Numar usi', 
					'Cutia de viteze', 
					'Kilometraj', 
					'Serie sasiu', 
					'Volan', 
					'Sarcina utila', 
					'Tara de origine', 
					'Compartimentare', 
					'Suprafata utila', 
					'Anul constructiei', 
					'Etaj Camere',
					'Mobilat', 
					'Extravilan / intravilan']

		details = ''
		time.sleep(random.randrange(2,3))
		res = requests.get(link,headers=HEADERS,proxies=proxies)
		details = bs(res.text, 'html.parser')

		with open('results.html', 'w', encoding='utf-8') as f:
			f.write(details.prettify())
		# with open('publi24/results.html', 'r', encoding='utf-8') as f:
		# 	details = bs(f, 'html.parser')

		title = details.find("meta", property="og:title")
		title = str(title['content']).replace('<br />', '').replace(u'\xa0','') if title else ''

		try:
			price_div = details.find('div', class_ = 'row detail-title')
			price =  price_div.find(itemprop = 'price').text.strip().replace(u'\xa0','')
			currency = price_div.find(itemprop = 'priceCurrency')['content'].strip()
		except:
			pass


		desc = details.find("meta", property="og:description")
		desc = str(desc['content']).replace(',', '3z@z3').replace('\n', '').replace('\r', '').replace(u'\xa0','').strip() if desc else ''

		username_div = details.find('div', class_ = 'userdata').find('h3', itemprop = 'name')
		username = username_div.text.strip()

		categories = details.find('div', id = 'breadcrumb-links').find_all('li')
		for cat in categories:
			cat = cat.text.strip()
			if cat in cat_ids['data']:
				cat_id = cat_ids['data'][cat]
				break

		location = details.find('div', class_ = 'row detail-info').find_all('a')
		city = location[1].text.strip()
		region = location[0].text.strip()

		try:
			specs = details.find('div', class_ = 'article-detail')
			specs_div= specs.find('div', class_ = 'row adproperties').find_all('div')

			for s in specs_div:
				spec = s.select('span')[0].find('strong').text.replace(',','') if s.select('span')[0].find('strong') else 'None'
				value = s.select('span')[1].text if len(s.select('span')) > 1 else 'None'
				specification = {"spec":spec.replace('\n','').strip(),"value":value.replace('\n','').replace('(6+1)','').strip()}
				if spec != 'None':
					specifications.append(specification)
		except:
			pass

		try:
			images = details.find('div', id = 'detail-gallery').find_all('img')
			image_link1 = details.find('figure', itemprop="associatedMedia").find('img')['src']
			image_link2 = images[1]['src']
		except:
			image_link1 = details.find('figure', itemprop="associatedMedia").find('img')['src']

		results.append(link)
		results.append(id)
		results.append(title)
		results.append(price)
		results.append(currency)
		results.append(cat_id)
		results.append(city)
		results.append(region)
		results.append(username)
		results.append(phone_number)
		results.append(desc)
		results.append(seller_type)
		check = False
		for f in features:
			if f == 'Volan' or f == 'Sarcina utila' or f == 'Tara de origine' or f == 'Extravilan / intravilan':
				results.append('')
				check = True
				continue
			else:	
				check = False
				for spec in specifications:
					if f == spec['spec']:
						spec = str(spec['value']).replace(' ','').replace('Verificakm!','').strip()
						if f == 'Suprafata utila':
							spec = spec.split(',')[0]
						re = ['cm³','CP','km','GB','m²','m2','0m²','0m2']
						for tag in re:
							if tag in spec:
								spec = spec.replace(tag,'').replace(' ', '')
						results.append(spec.capitalize())
						check = True
						break
					else:
						check = False
				if check is False:
					results.append('')

		image_links.append(image_link1)
		image_links.append(image_link2)
		for i in image_links:
			if i == 'none':
				results.append('')
				continue
			image_id = str(i).split('/')[7].replace('.jpg', '')
			new_image_link = f'MAMMAYA22MAMA/{image_id}.jpeg'
			results.append(new_image_link)

			time.sleep(2)
			print(i)
			download_image(i,image_id)

		results = [str(r).replace(',', '3z@z3').replace('\n', '').replace('\r', '') for r in results]
		return results,True
	except Exception as error:
		print(error)
		return [],False

def get_links(page):
	ad_types = ['false','true']
	ad_type = random.choice(ad_types)
	page = page

	HEADERS = {
		'authority': 'www.publi24.ro',
		'method': 'GET',
		"path": f"https://www.publi24.ro/anunturi/?commercial={ad_type}&pag={page}",
		'scheme': 'https',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding':'gzip, deflate, br',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
		'cache-control': 'max-age=0',
		'referer': f"https://www.publi24.ro/anunturi/?commercial={ad_type}",
		'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
	}
	payload = {
	'items': '100',
	'page': '2',
	'mobile':'true',
	'cursorMark':'*'
	}
	url = f"https://www.publi24.ro/anunturi/?commercial={ad_type}&pag={page}&pagesize=1"
	res = requests.get(url,headers=HEADERS,proxies=proxies)
	data = bs(res.text, 'html.parser')

	# with open('results.html', 'w', encoding='utf-8') as f:
	# 	f.write(data.prettify())

	details_div = data.find('ul', class_ = 'listing radius').find_all('li')
	ads = []
	for detail in details_div:
		try:
			link = detail.find('a')['href']

			id = str(link).replace('.html','').split('/')
			id = {"id":f"{id[len(id)-1]}"}
			if not id:
				continue
			phone = detail.find('div', class_ = 'hidden')['data-ph']
			phone = str(phone)
			if phone[0] != '0':
				phone = f"0{phone}"

			ads.append({"link":link,"id":id,"phone":phone,"ad_type":ad_type})
		except Exception as error:
			print(error)
			continue

	old_list = []
	new_list = []
	for ad in ads:
		if ad not in old_list:
			old_list.append(ad)
		else:
			print(f'---filtered {ad["id"]} from old_list')

	with open('ids_publi24.json', 'r+', encoding='utf-8') as f:
		file_data = json.load(f)
		for ad in old_list:
			id = ad['id']
			if id not in file_data['data']:
				new_list.append(ad)
				file_data['data'].append(id)
			else:
				print(f'Filtered: {id}')
		f.seek(0)
		json.dump(file_data, f, ensure_ascii=False, indent=4)

	len_data = len(new_list)
	print(len_data)
	with ThreadPoolExecutor(len_data) as executor:
		results = executor.map(get_list_details,new_list)
		with open('results_publi24.csv', 'a', encoding='utf-8',newline='') as file:
			for result in results:
				if result[1]:
					writer = csv.writer(file)
					writer.writerow(result[0])

def get_links():
	try:
		old_list = []
		new_list = []
		count = 500 
		page = 0
		while len(new_list) < 100:
			pages = [i + page for i in range(3)]
			ads = []
			with ThreadPoolExecutor(len(pages)) as executor:
				results = executor.map(get_data,pages) 
				for result in results:
					if result[1]:
						ads += result[0]
					else:
						print(result[0])
			for ad in ads:
				if ad not in old_list:
					old_list.append(ad)
				else:
					print(f'---filtered {ad["id"]} from old_list')

			with open('ids_publi24.json', 'r+', encoding='utf-8') as f:
				file_data = json.load(f)
				for ad in old_list:
					if len(new_list) < 100:
						id = ad['id']
						if id not in file_data['data']:
							new_list.append(ad)
							file_data['data'].append(id)
						else:
							print(f'Filtered: {id}')
					else:
						break
				f.seek(0)
				json.dump(file_data, f, ensure_ascii=False, indent=4)
				page += 3
				print(len(new_list))
		len_data = len(new_list)
		print(len_data)
		with ThreadPoolExecutor(len_data) as executor:
			results = executor.map(get_list_details,new_list)
			with open('../results/results_publi24.csv', 'a', encoding='utf-8',newline='') as file:
				for result in results:
					print(result[2])
					if result[1]:
						writer = csv.writer(file)
						writer.writerow(result[0])
	except Exception as error:
		print(error)
		return
			

if __name__ == '__main__':
	main(0)



