from bs4 import BeautifulSoup
from Opener import opener
import requests
import json

name = 'welt'

def get_opener():
    # get link to opener
    url = 'https://www.welt.de/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    opener_link = url[:-1] + soup.find("section").find(class_='o-headline').find_parent('a')['href']

    # get data on opener
    response = requests.get(opener_link, headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    # meta tags have headline and keywords
    headline = soup.find('title').text[:-7]
    keywords = soup.find('meta', {"name":"keywords"})['content'].split(', ')

    # structured data
    data = str(soup.find("script", {"type":"application/ld+json", "data-qa":"StructuredData"}))\
        .split('>', 1)[1].split('</script>')[0]
    data = json.loads(data)
    authors = [data.get('author')['name']]
    ressort = data.get('category')

    # subressort is in breadcrumb
    breadcrumb = soup.find('div', {"class":"c-breadcrumb"})\
                     .find_all('li')

    if len(breadcrumb) > 3:
        sub_ressort = breadcrumb[2].text.strip()
    else:
        sub_ressort = None

    op = opener(headline, opener_link, authors, ressort, sub_ressort, keywords, name)
    return op