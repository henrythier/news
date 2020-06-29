from bs4 import BeautifulSoup
import requests

author_tag = '\'contentAuthor\': '
ressort_tag = '\'pageCategoryLevel2\': '
sub_ressort_tag = '\'pageCategoryLevel3\': '

def find_tag(soup, tag, offset):
    for s in soup.find_all("script"):
        s = str(s)
        start = s.find(tag)
        if start == -1:
            continue
        else:
            end = s.find('\',', start)
            start = start + len(tag) + offset
            result = s[start:end]
            return result

def get_opener():
    from Opener import opener
    # get link
    url = 'https://www.t-online.de/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = soup.findAll(class_="Ttsi")[0].find('a')['href']

    # get keywords, headline, author
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    keywords = soup.find("meta", {"name":"keywords"})['content'].split(', ')
    headline = soup.find("title").text

    # find authors
    authors = find_tag(soup, author_tag, 1)
    authors = authors.split(', ')

    # find ressort
    ressort = find_tag(soup, ressort_tag, 1)

    # find subressort
    sub_ressort = find_tag(soup, sub_ressort_tag, 1)

    # into object
    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, 't-online')
    return op