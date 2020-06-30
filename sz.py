from bs4 import BeautifulSoup
from Opener import opener
import requests
import json

name = 'sz'


def get_opener():
    url = 'https://www.sueddeutsche.de/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}

    # get link to opener
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = soup.find("main").find('a')['href']

    # get data on opener
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    # headline, keywords and authors are in meta tags
    headline = soup.find("meta", {"property": "og:title"})['content']
    keywords = soup.find("meta", {"name": "keywords"})['content'].split(',')
    authors = soup.find_all("meta", {"name":"author"})
    authors = [a['content'] for a in authors]

    # ressort is in java script
    data = soup.find("script", {"type":"text/javascript"})
    data = str(data).split('[')[1].split(']')[0]
    data = json.loads(data)
    ressort = data.get("ressort")
    sub_ressort = data.get("thema")

    # initialise opener
    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, name)
    return op

