from multiprocessing.pool import ThreadPool
import feedparser
import sqlite3


filepath = '/Users/Rahul/Desktop/Side_projects/crypto_in_one/crypto/files/urls'
f = open(filepath)
hit_list = [i.replace('\n', '') for i in f.readlines()]
print(hit_list)

def parse_feed(feed_url):  # Todo: Dictionary possible?
    result = []
    parsed_feed = feedparser.parse(feed_url)
    for story in parsed_feed.get('entries'):
        title = story.get('title')
        link = story.get('link')
        # category = categorize(feed_url)
        result.append([title, link])
    return result


conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/crypto_in_one/db.sqlite3', check_same_thread=False)
c = conn.cursor()


def feed_execute(parsed_feed):
    c.execute('SELECT MAX(id) FROM crypto_feeds')
    recent_primary_key = c.fetchone()
    if recent_primary_key[0] is None:
        recent_primary_key = 1
    else:
        recent_primary_key = recent_primary_key[0]

    for number in range(len(parsed_feed)):
        recent_primary_key += 1
        title = parsed_feed[number][0]
        link = parsed_feed[number][1]
        c.execute("INSERT INTO crypto_feeds VALUES (?, ?, ?)",
                  (recent_primary_key, title, link))
        conn.commit()
    print('RSS Done')


def run_it():
    """ Main function used in Django view to fetch all rss feeds"""
    c.execute("DELETE FROM crypto_feeds")
    conn.commit()
    pool = ThreadPool()
    results = pool.map(parse_feed, hit_list)
    for result in results:
        feed_execute(result)
