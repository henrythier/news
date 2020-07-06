from bs4 import BeautifulSoup
from Opener import opener
import requests
import json

name = 'Zeit'
author_tag = '\'contentAuthor\': '
ressort_tag = 'ressort\': '
sub_ressort_tag = 'sub_ressort\': '

def find_tag(soup, tag, offset):
    for s in soup.find_all("script"):
        s = str(s)
        start = s.find(tag)
        if start == -1:
            continue
        else:
            end = s.find('\",', start)
            start = start + len(tag) + offset
            result = s[start:end]
            return result

def get_opener():
    url = 'https://www.zeit.de/index'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = soup.find(id='main').find("a")['href']

    # get keywords, headline, author
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    keywords = soup.find("meta", {"name":"keywords"})['content'].split(', ')
    headline = soup.find("title").text.split(' |')[0]

    soup = BeautifulSoup(response.text, features="html.parser")
    data = soup.find_all('script', type='application/ld+json')

    for d in data:
        inner_script = str(d)[36:-10]
        json_script = json.loads(inner_script)
        authors = json_script.get('author')
        if authors is None:
            continue
        else:
            try:
                authors_temp = [a.get('name') for a in authors]
            except AttributeError:
                authors_temp = [authors.get('name')]

            authors = authors_temp
            break

    ressort = find_tag(soup, ressort_tag, 1)
    sub_ressort = find_tag(soup, sub_ressort_tag, 1)
    if len(sub_ressort) == 0:
        sub_ressort = None

    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, name)
    return op


'''
Different css classes containing link to opener
opener_link = soup.find(class_="zon-teaser-classic__combined-link")['href']
opener_link = soup.find(class_="zon-teaser-lead__combined-link")['href']
opener_link = soup.find(class_="zon-teaser-poster__combined-link")['href']
'''
