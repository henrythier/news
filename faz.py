from bs4 import BeautifulSoup
from Opener import opener
import requests
import json

def get_opener():
    url = 'https://www.faz.net/aktuell/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = soup.find(class_="js-hlp-LinkSwap js-tsr-Base_ContentLink tsr-Base_ContentLink")['href']

    # get keywords, headline, author
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    keywords = soup.find("meta", {"name":"keywords"})['content'].split(', ')
    headline = soup.find("title").text

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

    data = soup.find(class_="js-adobe-digital-data is-Invisible")['data-digital-data']
    data = json.loads(data)
    ressort = data.get('page').get('ressort')
    sub_ressort = data.get('page').get('subressort1')

    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, 'faz')
    return op