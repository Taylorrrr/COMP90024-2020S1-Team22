import utils
from pprint import pprint
from collections import OrderedDict
import requests
import json

db = utils.db(url='45.88.195.224:9001', name='tweets')
url = 'http://admin:admin@45.88.195.224:9001/tweets/_design/list/_list/filter/hashtag/count?group_level=1&limit=20000&threshold=5000'
# resp = json.loads(requests.get(url, stream=True).content)
# db = utils.db(url='localhost:5984', name='tweet-stream')
# header, resp = db.list('process/sorted', '90024/hashtag', group_level=1, limit=200, top=10)
# pprint(resp)
# header, resp = db.list('list/filter', 'hashtag/count', group_level=1, limit=20000, threshold=5000)
for l in utils.stream(url):
    print(l)
# d = {r['key']: r['value'] for r in resp['rows']}
# for l in d.items():
#     print(l)
# print(sum([v for v in d.values()]))

# with open('list.txt', 'r') as f:
#     l = f.read()
#     print(repr(l))