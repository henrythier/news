from bs4 import BeautifulSoup
from Opener import opener
import requests

name = 'ntv'

def get_opener():
    url = 'https://www.n-tv.de/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = soup.find('section', {"class":"group"}).find('a')['href']

    # get keywords, headline, author from meta
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    headline = soup.find("title").text.rsplit(' - ', 1)[0]
    keywords = soup.find("meta", {"name":"news_keywords"})['content'].split(', ')
    authors = [a['content'] for a in soup.find_all("meta", {"name":"author"})]

    # get ressort from breadcrumb
    breadcrumbs = soup.find("nav", {"class":"breadcrumb"}).find_all('a')
    ressort = breadcrumbs[1].text.strip()

    if len(breadcrumbs) > 2:
        sub_ressort = breadcrumbs[2].text.strip()
    else:
        sub_ressort = None

    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, name)
    return op