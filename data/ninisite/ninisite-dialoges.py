
import json
from os.path import isfile, join
from os import listdir
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm
import ray
import sys
sys.setrecursionlimit(100000)

def get_first_page(url): 
    topic_url = urlopen(url+'?page=1')
    topic_content = topic_url.read()
    topic_soup = BeautifulSoup(topic_content, 'html.parser')
    pagination = topic_soup.find_all('a',{'class':'page-link'}) 
    pages = 1 if len(pagination) == 0 else int(pagination[-2].text)
    return pages, topic_soup

def read_files_get_urls(path):
    categories_url_path =  [f for f in listdir(path) if isfile(join(path, f))]
    all_topics = []
    for cat in categories_url_path:
        with open('topics/all_topics.jsonl', 'a', encoding="utf-8") as outfile:
            with open(f'topics/{cat}') as jsonl:
                topics = jsonl.readlines()
                for d in topics:
                    all_topics.append((cat, d.strip()))
                    try:
                        json.dump((cat, eval(d)), outfile, ensure_ascii=False)
                        outfile.write('\n')             
                    except:
                        pass
                       

def read_jsonl(path):
    with open(path) as jsonl:
        craweld_topics = jsonl.readlines()
        craweld_topics = [eval(t.strip()) for t in craweld_topics]
    return craweld_topics

def get_soup(url):
    topic_url = urlopen(url)
    topic_content = topic_url.read()
    soup = BeautifulSoup(topic_content, 'html.parser')
    return soup

def get_p(page):
    return [p.text for p in page.find('div',{'class':'post-message'}).find_all('p')]

@ray.remote
def crawl(p, pages, topic_soup, topic_url_string):
        conv = []
        if pages > 1:
            topic_soup = get_soup(topic_url_string+f'?page={p}')
        
        for i, article in enumerate(topic_soup.find_all('article')):
            message = get_p(article)

            reply_message_div = article.find('div',{'class':'reply-message'})
            reply_message_text = reply_message_div.text if reply_message_div else None
            
            if reply_message_text != None:
                if len(reply_message_text)  < 90:
                    reply_message = reply_message_text
                else:
                    reply_message_id = reply_message_div['data-id'] if reply_message_div else None
                    
                    if reply_message_id != None:
                        reply_message = topic_soup.find('article', attrs={'id':f'post-{reply_message_id}'})
                        
                        if reply_message != None:
                            reply_message = get_p(reply_message)
                        else:
                            reply_message_url_string = topic_url_string+f'?postId={reply_message_id}'
                            reply_message_soup = get_soup(reply_message_url_string)

                            reply_message = reply_message_soup.find('article', attrs={'id':f'post-{reply_message_id}'})
                            if reply_message != None:
                                reply_message = get_p(reply_message)
                            else:
                                reply_message = 'None'
            else:
                reply_message = topic_soup.find('article', attrs={'id':'topic'})
                reply_message_title = topic_soup.find('article', attrs={'id':'topic'}).find('h1',{'class':'topic-title'}).find('a').text
                reply_message = get_p(reply_message)

            if i != 0:
                conv.append({
                        "topic": reply_message_title,
                        "question":reply_message,
                        "answer":message,
                    })
        return conv


def parallel_crawler(topics):
    ray.init()

    crawled_topics = open('topics/all_crawled_topics.jsonl', 'a', encoding="utf-8")

    for i, topic in tqdm(enumerate(topics)):

        topic_url_string ='https://ninisite.com/'+ topic[1]['url']
        pages, topic_soup = get_first_page(topic_url_string)

        conv = [crawl.remote(p, pages, topic_soup, topic_url_string) for p in range(1, pages+1)]
        conv = ray.get(conv)
        conv = sum(conv,[])

        with open(f'dialogue/{topic[0]}', 'a', encoding="utf-8") as outfile:
            for c in conv:
                json.dump(c, outfile, ensure_ascii=False)
                outfile.write('\n')

        json.dump((topic[0], topic[1]), crawled_topics, ensure_ascii=False)
        crawled_topics.write('\n')

    crawled_topics.close()
     


if __name__ == "__main__":
    # read_files_get_urls('topics')
    all_topics = read_jsonl('topics/all_topics.jsonl')
    craweld_topics = read_jsonl('topics/all_crawled_topics.jsonl')
    remained_topics = [item for item in all_topics if item not in craweld_topics]
    print (f"{len(all_topics)} All Topics", f"{len(craweld_topics)} Crawled", f"{len(remained_topics)} Remained")
    parallel_crawler(craweld_topics)
