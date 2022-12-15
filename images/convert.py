import concurrent.futures
from http import client
from multiprocessing.connection import Client
import time
from datetime import datetime
from PIL import Image
import csv
import requests
import os
import boto3
from dotenv import load_dotenv
from os import listdir
from os.path import isfile
from botocore.exceptions import ClientError

load_dotenv()

access_key = os.getenv("ACCESS_KEY")
access_secret = os.getenv("ACCESS_SECRET")
bucket = 'greg-media-storage'

links = []

# with open('images/image_links.csv', 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for r in reader:
#         if r:
#             r = str(r).replace("', '']", '').replace("['",'')
#             image_id = r.split('/')[5].replace('-RO', '')
#             links.append({'link':r, 'id': image_id})


# f = open('images/image_links.csv', 'w+')
# f.close()

# def download_image(link):
#     try:
#         url = link['link']
#         id = link['id']
#         with open(f'images/image_files/{id}.jpeg', 'wb') as f:
#             image = requests.get(url)
#             f.write(image.content)
#     except Exception as error:
#         print(error)

# with concurrent.futures.ThreadPoolExecutor(len(links)) as executor:
#     print('Downloading .....')
#     results = executor.map(download_image,links)
#print('Done .....')

today = datetime.today().strftime('%Y-%m-%d')
client1 = boto3.client(
    's3', 
    aws_access_key_id = access_key, 
    aws_secret_access_key = access_secret)

def upload(image):
    upload_link = f'{today}/{image}'
    try:
        client1.upload_file(
            os.path.abspath(f'./images/image_files/{image}'),
            bucket,
            upload_link,
            ExtraArgs={'ACL': 'public-read', "ContentType": "image/jpeg"}
        )

        time.sleep(2)
        os.remove(os.path.abspath(f'./images/image_files/{image}'))
    except ClientError as e:
        print('credential error')
        print(e)
        return
    except Exception as e:
        print(e)
        return

image_folder = os.path.abspath('./images/image_files/')
images = [image for image in listdir(image_folder) if isfile(f"{image_folder}/{image}")]

with concurrent.futures.ThreadPoolExecutor(len(images)/10) as executor:
    print('Uploading .....')
    results = executor.map(upload,images)
print('Done .....')
