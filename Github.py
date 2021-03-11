import requests
from bs4 import BeautifulSoup


def setup():
    repos = ['BooksDatabase1', 'BooksDatabase2']

    links = []
    for repo in repos:
        response = requests.get('https://github.com/Colby-Wilson/' + repo)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', title=True, href=True):
                if 'tree/master' in str(link):
                    if len(link['href'].split('/')) == 7:
                        link['href'] = link['href'][:-2]
                        link['title'] = link['href'].split('/')[5]
                    links.append(link)
    return links

def content(repos, name):
    for repo in repos:
        if repo['title'] == name:
            response = requests.get('https://github.com/' + repo['href'])
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                sub = []
                for dir in soup.find_all('a', title=True, href=True):
                    # print(dir)
                    if 'tree/master' in str(dir):
                        sub.append(dir['href'])
                chapters = []
                for dir in sub:
                    response = requests.get('https://github.com' + dir)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        for issue in soup.find_all('a', title=True, href=True):
                            if 'blob/master' in str(issue):
                                chapters.append(issue)
                return chapters

