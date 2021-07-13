from celery import Celery
import requests, time, cssselect
from lxml import html
from collections import Counter

from db import insert

app = Celery('tasks')

@app.task
def parse(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    all_elms = tree.cssselect('*')
    all_tags = [x.tag for x in all_elms]
    c = Counter(all_tags)
    print(c)
    print(type(c))
    global tag
    for e in c:
        if e == 'div': tag = c[e]

    print(tag)
    time.sleep(1)
    return tag
