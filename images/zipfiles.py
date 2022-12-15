from datetime import datetime
import shutil
import time
import csv
import os
from os import listdir
from os.path import isfile


with open('wait_check.csv','w') as check:
    check.write('1')

today = datetime.today().strftime('%Y-%m-%d')
now = datetime.now()
current_time = now.strftime("%H:%M")

results = []
results2 = []
with open('../results/results.csv', 'r') as f:
    reader = csv.reader(f)
    results += reader

with open('../results/results_publi24.csv', 'r') as f2:
    reader = csv.reader(f2)
    results2 += reader

shutil.make_archive(f'{today}', 'zip', '../results')

time.sleep(2)
shutil.make_archive(f'{today}-images-olx', 'zip', 'image_files')

time.sleep(2)
shutil.make_archive(f'{today}-images-publi24', 'zip', 'image_files_publi24')

image_folder = os.path.abspath('image_files')
images = [image for image in listdir(image_folder) if isfile(f"{image_folder}/{image}")]

image_folder2 = os.path.abspath('image_files_publi24')
images2 = [image for image in listdir(image_folder2) if isfile(f"{image_folder2}/{image}")]

for image in images:
    os.remove(os.path.abspath(f'image_files/{image}'))

for image in images2:
    os.remove(os.path.abspath(f'image_files_publi24/{image}'))

with open('../results/results.csv', 'w+') as r_f:
    pass
with open('../results/results_publi24.csv', 'w+') as r_f2:
    pass

with open('../submitted.csv', 'a') as file:
    file.write(f'{len(results)},{today}\n')
    file.write(f'{len(results2)},{today}\n')

with open('wait_check.csv','w') as c:
    c.write('0')
    