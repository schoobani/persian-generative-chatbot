from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from tqdm import tqdm


def get_topic_url(soup):
    topic_urls = []
    for i, title in enumerate(soup.find_all('div',{'class':'category--header'})):
        icon = True if title.find('i') else False
        if not icon:
            if int(title.find('span',{'class':'topic_number'}).text) > 5:
                topic_urls.append(
                    {
                    'title':title.find('a').text.strip(),
                    'url':title.find('a')['href'].strip()
                }
                )
    return topic_urls


with open('topics/family-solutions.jsonl', 'a', encoding="utf-8") as outfile:
    for n in tqdm(range(1, 4000)):
        category_topics_url_string = ''
        category_topics_url = urlopen(category_topics_url_string+f'?page={n}')
        category_topics = category_topics_url.read()
        category_topics_soup = BeautifulSoup(category_topics, 'html.parser')
        topic_urls = get_topic_url(category_topics_soup)
        for url in topic_urls:
            json.dump(url, outfile, ensure_ascii=False)
            outfile.write('\n')