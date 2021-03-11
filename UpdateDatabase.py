import requests
from bs4 import BeautifulSoup
import sqlite3
import Github as g


repos = g.setup()

try:
    conn = sqlite3.connect('D:/Books/BookDatabase')
except:
    try:
        conn = sqlite3.connect('//MAIN-DESKTOP/Books/BookDatabase')
    except:
        conn = sqlite3.connect('BookDatabase')
crsr = conn.cursor()

for repo in repos:
    print(repo['title'])
    try:
        crsr.execute('create table ' + repo['title'] + ' (Issue float, Address nvarchar(255), Read bit);')
    except:
        pass
    chapters = g.content(repos, repo['title'])
    for chapter in chapters:
        crsr.execute('select 1 from ' + repo['title'] + ' where Issue=' + chapter['title'].split(' ')[len(chapter['title'].split(' ')) - 1][:-4])
        exists = crsr.fetchall()
        if exists:
            crsr.execute('update ' + repo['title'] + ' set Address="https://github.com' + chapter['href'] + '" where Issue=' + chapter['title'].split(' ')[len(chapter['title'].split(' ')) - 1][:-4])
        else:
            crsr.execute('insert into ' + repo['title'] + ' (Issue, Address, Read) values (' + chapter['title'].split(' ')[len(chapter['title'].split(' ')) - 1][:-4] + ', "https://github.com' + chapter['href'] + '", 0)')


conn.commit()
conn.close()