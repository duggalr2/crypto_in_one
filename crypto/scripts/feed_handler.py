from multiprocessing.pool import ThreadPool
import feedparser
import sqlite3
from time import mktime
from datetime import datetime
# from scr.category_rss import classify, read_dataset
from crypto.scripts import category_rss

FILEPATH = '/Users/Rahul/Desktop/Side_projects/crypto_in_one/uci_news.csv'
conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/crypto_in_one/db.sqlite3', check_same_thread=False)
c = conn.cursor()
c.execute('SELECT url FROM crypto_feedurl')
url_list = c.fetchall()
hit_list = [url[0] for url in url_list]


def parse_feed(feed_url):
    result = []
    X, y = category_rss.read_dataset(FILEPATH)
    m, v = category_rss.train_model_save(X, y)
    parsed_feed = feedparser.parse(feed_url)
    for story in parsed_feed.get('entries'):
        title = story.get('title')
        category = category_rss.classify(X, y, title, m, v)
        link = story.get('link')
        last_timestamp = story.get('updated_parsed')
        result.append([title, link, last_timestamp, feed_url, category])
    return result


def add_url(url):
    c.execute('SELECT MAX(id) FROM crypto_feedurl')
    recent_primary_key = c.fetchone()
    if recent_primary_key[0] is None:
        recent_primary_key = 1
    else:
        recent_primary_key = recent_primary_key[0]
    c.execute('INSERT INTO crypto_feedurl (id, url) VALUES (?, ?)', (recent_primary_key+1, url))
    conn.commit()


def feed_execute(parsed_feed):
    c.execute('SELECT MAX(id) FROM crypto_feeddetail')
    recent_primary_key = c.fetchone()
    if recent_primary_key[0] is None:
        recent_primary_key = 1
    else:
        recent_primary_key = recent_primary_key[0]

    for number in range(len(parsed_feed)):
        recent_primary_key += 1
        title = parsed_feed[number][0]
        link = parsed_feed[number][1]
        struct = parsed_feed[number][2]
        dt = datetime.fromtimestamp(mktime(struct))
        time = dt.strftime('%H:%M:%S')
        feed_url = parsed_feed[number][-2]
        category = parsed_feed[number][-1]
        c.execute("INSERT INTO crypto_feeddetail (id, feed_url_id, title, story_url, timestamp, category) VALUES (?, ?, ?, ?, ?, ?)",
                  (recent_primary_key, feed_url, title, link, time, category))
        conn.commit()
    print('RSS Done')


def run_it():
    """ Main function used in Django view to fetch all rss feeds"""
    c.execute("DELETE FROM crypto_feeddetail")
    conn.commit()
    pool = ThreadPool()
    results = pool.map(parse_feed, hit_list)
    for result in results:
        feed_execute(result)

# if __name__ == '__main__':
#     run_it()

# f = open('/Users/Rahul/Desktop/Side_projects/crypto_in_one/crypto/files/urls2')
# lines = f.readlines()
# url_list = [line.replace('\n', '') for line in lines]
# for url in url_list:
#     add_url(url)


