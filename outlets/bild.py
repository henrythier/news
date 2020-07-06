from bs4 import BeautifulSoup
from Opener import opener
import requests
import json
import re

name = 'bild'
ressort_tag = '\"subChannel1\" : '
sub_ressort_tag = '\"subChannel2\" : '

def find_tag(soup, tag, offset):
    for s in soup.find_all('script'):
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
    url = 'https://www.bild.de/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)

    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = url[:-1] + soup.find(id='innerContent').find("a")['href']

    # get keywords, headline, author
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    keywords = soup.find("meta", {"name":"keywords"})['content'].split(',')
    data = soup.find_all('script', type='application/ld+json')

    for d in data:
        inner_script = str(d)[36:-10]
        json_script = json.loads(inner_script)
        headline = json_script.get('headline')
        authors = json_script.get('author')
        if authors is None:
            continue
        else:
            try:
                authors_temp = authors[0].get('name')
                authors_temp = re.split(' und |, ', authors_temp)
            except KeyError:
                authors_temp = ['Organisation']

            authors = authors_temp
            break

    if headline is None:
        headline = soup.find("title").text
        headline = headline.rsplit('-', 2)[0]
        headline = headline.strip()

    ressort = find_tag(soup, ressort_tag, 1)
    sub_ressort = find_tag(soup, sub_ressort_tag, 1)

    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, name)
    return op