import Github as g
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import shutil
from PIL import Image
from PIL import ImageFile
from threading import Thread
ImageFile.LOAD_TRUNCATED_IMAGES = True

op = webdriver.ChromeOptions()
op.add_argument('headless')


driverA = webdriver.Chrome()
driverB = webdriver.Chrome()
driverA.get('http://mangareader.cc')
driverB.get('http://readallcomics.com/')
if os.path.exists('targets.txt'):
    print('Previous Targets')
    for link in open('targets.txt', 'r').readlines():
        print(link.replace('\n', ''))

f = open('targets.txt', 'a+')
targets = []
while True:
    inputTarget = input('Page :')
    if inputTarget == '':
        break
    f.write(inputTarget + '\n')
f.close()
driverA.close()
driverB.close()
targets = open('targets.txt', 'r').readlines()

try:
    os.mkdir('Output')
except:
    pass

repos = g.setup()


def pullManga(target):
    name = target.split('/')[len(target.split('/')) - 1].replace('-', '')
    response = requests.get(target)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True, title=True)
        links.pop(0)
        links = links[::-1]
        links.pop(0)
        try:
            if links[0]['class'][0] == 'xanh':
                links.pop(0)
                links.pop(0)
        except:
            pass
        r = g.content(repos, name)
        if r is None:
            try:
                os.mkdir('Output/' + name)
            except:
                pass
        for link in links:
            try:
                if link['title'] in str(r).replace('&amp;', '&'):
                    continue
                else:
                    print(link['title'] + '/' + str(len(links)))
                    try:
                        os.mkdir(name)
                    except:
                        shutil.rmtree(name)
                        os.mkdir(name)
                    driver = webdriver.Chrome(options=op)
                    driver.get(link['href'])
                    try:
                        select = Select(driver.find_elements_by_tag_name('select')[1])
                    except:
                        print('Failed : ' + link['title'])
                        continue
                    select.select_by_index(1)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    driver.close()
                    picture = 0
                    for pic in soup.find_all('img'):
                        if 'lazy' in str(pic):
                            picture += 1
                            response = requests.get(pic['src'])
                            file = open(name + '/' + str(picture) + '.jpg', 'wb')
                            file.write(response.content)
                            file.close()
                    images = os.listdir(name)
                    images = sorted(images, key=lambda x: int(x[:-4]))
                    pics = []
                    for image in images:
                        pics.append(Image.open(name + '/' + image))
                    pic1 = pics[0]
                    pics.pop(0)
                    pic1.save('Output/' + link['title'] + '.pdf', 'PDF', resolution=100.0, save_all=True, append_images=pics)
                    shutil.rmtree(name)
            except Exception as e:
                print(e)
                continue






def pullComic(target):
    name = target.split('/')[len(target.split('/')) - 2].replace('-', '')
    response = requests.get(target)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True, title=True)
        links.pop(0)
        links.pop(0)
        links = links[::-1]
        links.pop(0)

        r = g.content(repos, name)
        if r is None:
            try:
                os.mkdir('Output/' + name)
            except:
                pass
        issue = 0
        for link in links:
            try:
                issue += 1
                link['title'] = link['title'].replace('.', '').replace('…', '').replace(':', '').replace('#', '').replace('/', '').replace('?', '')
                if link['title'][len(link['title']) - 1] != ' ':
                    link['title'] = link['title'] + ' '
                link['title'] = link['title'] + str(issue)
                if link['title'] in str(r).replace('&amp;', '&'):
                    continue
                else:
                    print(link['title'] + '/' + str(len(links)))
                    try:
                        os.mkdir(name)
                    except:
                        shutil.rmtree(name)
                        os.mkdir(name)
                    response = requests.get(link['href'])
                    soup = BeautifulSoup(response.content, 'html.parser')
                    picture = 0
                    for pic in soup.find_all('img'):
                        if 'blogspot' in str(pic):
                            picture += 1
                            response = requests.get(pic['src'])
                            file = open(name + '/' + str(picture) + '.jpg', 'wb')
                            file.write(response.content)
                            file.close()
                    images = os.listdir(name)
                    images = sorted(images, key=lambda x: int(x[:-4]))
                    pics = []
                    for image in images:
                        pics.append(Image.open(name + '/' + image))
                    pic1 = pics[0]
                    pics.pop(0)
                    pic1.save('Output/' + link['title'] + '.pdf', 'PDF', resolution=100.0, save_all=True,
                              append_images=pics)
                    shutil.rmtree(name)
            except Exception as e:
                print(e)
                continue

threads = []
for target in targets:
    target = target.replace('\n', '')
    if 'http://mangareader.cc' in target:
        threads.append(Thread(target=pullManga, args=(target,)))
    elif 'http://readallcomics.com/' in target:
        threads.append(Thread(target=pullComic, args=(target,)))

issue = 0
# while True:
#     if issue + 10 > len(threads):
#         break
#     for i in range(0, 10):
#         threads[issue + i].start()
#     for thread in threads:
#         while thread.is_alive():
#             pass
#     issue += 10
while issue < len(threads):
    threads[issue].start()
    issue += 1

for thread in threads:
    while thread.is_alive():
        pass  

print('\n\n\n\n\nDONE')