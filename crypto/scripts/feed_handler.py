from multiprocessing.pool import ThreadPool
import feedparser
import sqlite3


def parse_feed(feed_url):
    result = []
    parsed_feed = feedparser.parse(feed_url)
    for story in parsed_feed.get('entries'):
        title = story.get('title')
        link = story.get('link')
        # original_story_date = story.get('created_parsed')
        last_timestamp = story.get('updated_parsed')
        result.append([title, link, last_timestamp, feed_url])
    return result

conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/crypto_in_one/db.sqlite3', check_same_thread=False)
c = conn.cursor()
c.execute('SELECT url FROM crypto_feedurl')
url_list = c.fetchall()
hit_list = [url[0] for url in url_list]


from time import mktime
from datetime import datetime


# l = parse_feed(hit_list[0])
# for i in l:
#     struct = i[-1]
#     dt = datetime.fromtimestamp(mktime(struct))
#     time = dt.strftime('%H:%M:%S')


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
        feed_url = parsed_feed[number][-1]
        c.execute("INSERT INTO crypto_feeddetail (id, feed_url_id, title, story_url, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (recent_primary_key, feed_url, title, link, time))
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
# run_it()
# feed_url = models.ForeignKey(FeedUrl, on_delete=models.CASCADE)
#     title = models.CharField(max_length=1000)
#     story_url = models.URLField()
#     timestamp = models.TimeField()


