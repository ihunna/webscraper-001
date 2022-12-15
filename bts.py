from bs4 import BeautifulSoup as bs
import requests
import csv

username = 'massive123'
password = 'ekedende'


proxy = f'http://{username}:{password}@us.smartproxy.com:10000'
def find_links():
    url = 'https://www.olx.ro/auto-masini-moto-ambarcatiuni/?view=galleryWide'
    res = requests.get(url)

    data = bs(res.text, 'html.parser')
    print(data)

    next_btn_list = data.find('div', class_='pager rel clr')

    span = next_btn_list.find_all('span', class_ = 'item fleft')
    total = span[len(span) - 1].find('span')
    total = int(str(total.string).strip())
    all_links = []
    i = 1
    for i in range(1,total):
        ul = data.find('ul', id = 'gallerywide')
        links = ul.find_all('div', class_ = 'inner')
        for li in links:
            a = li.find('a')
            link = a['href']
            all_links.append(link)
            # print(link)
        ul2 = data.find('ul', id = 'gallerywide2')
        links2 = ul2.find_all('div', class_ = 'inner')
        for li in links2:
            a = li.find('a')
            link = a['href']
            all_links.append(link)
            # print(link)
        url = f'https://www.olx.ro/auto-masini-moto-ambarcatiuni/?view=galleryWide&page={str(i + 1)}'
        res = requests.get(url)
        data = bs(res.text, 'html.parser')
        print(f'---:page: {i + 1}')

    for link in all_links:
        print(link)

    with open('links.csv', 'w') as f:
        for link in all_links:
            f.write(link)
            f.write(',')
            f.write('\n')
find_links()