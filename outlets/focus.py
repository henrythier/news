from bs4 import BeautifulSoup
from Opener import opener
import requests

name = 'focus'
ressort_tag = "\'pageLevel1\'"
sub_ressort_tag = "\'pageLevel2\'"

def find_tag(tag, response):
    start = response.text.find(tag)
    end = response.text[start:].find('\n')
    text = response.text[start:start + end].split(':')[1].strip()[1:-2]
    return text

def get_opener():
    url = 'https://www.focus.de/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = soup.find(id='topArticle').find('a')['href']

    # get keywords, headline, author
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    headline = soup.find("title").text.rsplit(' - ', 2)[0]
    keywords = soup.find("meta", {"name":"news_keywords"})['content'].split(', ')
    authors = [a['content'] for a in soup.find_all("meta", {"name":"author"})]

    # find ressorts
    ressort = find_tag(ressort_tag, response)
    sub_ressort = find_tag(sub_ressort_tag, response)

    # initialise opener instance
    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, name)
    return op
