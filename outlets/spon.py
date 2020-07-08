from bs4 import BeautifulSoup
from Opener import opener
import requests
import json
import sys

name = 'spon'

# wrapper function to deal with different states
def find_opener_link(soup, flist):
    err = None
    for f in flist:
        try:
            ol = f(soup)
            if ol is not None:
                return ol
        except:
            err = sys.exc_info()[0]
            continue
    raise Exception('{}: Could not find opener link'.format(err))


def find_by_bold_text(soup):
    # title is first element with font-extrabold class
    return soup.find('main').find("span", class_="font-extrabold").find_parent('a')['href']


def find_by_article(soup):
    # title is in first article tag
    return soup.find('main').find('article').find('a')['href']


def find_by_h2_tag(soup):
    # title is in second h2 tag
    return soup.find("main").findAll('h2')[1].find('a')['href']


def find_first_a(soup):
    # link is in first a tag
    return soup.find("main").find('a')['href']


def get_opener():
    flist = [find_by_article, find_by_bold_text, find_by_h2_tag, find_first_a]
    url = 'https://www.spiegel.de/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = find_opener_link(soup, flist)

    # get keywords, headline, author
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    headline = soup.find('title').text.strip().split('DER SPIEGEL')[0][:-3]
    authors = soup.find("meta", {"name":"author"})['content'].split(', ')
    authors = authors[0] if len(authors) == 1 else authors[:-1]
    keywords = soup.find("meta", {"name":"news_keywords"})['content'].split(', ')

    # structured data
    # <script type="application/ld+json">
    data = soup.find("script", {"type":"application/ld+json"})
    data = str(data).split('>', 1)[1]
    data = data.split('</script>')[0]
    data = json.loads(data)

    ressort = data[0].get('articleSection')
    sub_ressort = data[1].get("itemListElement")

    sub_ressort = [a.get('item').get('name') for a in sub_ressort]
    if len(sub_ressort) > 3:
        sub_ressort = sub_ressort[2]
    else:
        sub_ressort = None

    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, name)

    return op

