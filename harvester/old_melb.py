import utils
import json
from pprint import pprint


def gen(f):
    yield from filter(None, map(parse_line, f))


def parse_line(line):
    try:
        line = line.strip()
        if line.endswith(','):
            line = line[:-1]
        return json.loads(line)['doc']
    except json.decoder.JSONDecodeError:
        pass


def parse_user(raw_user):
    user = {}
    user['_id'] = raw_user['id_str']
    user['type'] = 'user'
    user['name'] = raw_user['screen_name']
    user['level'] = 0
    user['expanded'] = False
    user['searched'] = False
    for key in ['followers_count', 'friends_count', 'statuses_count']:
        user[key] = raw_user[key]

    return None if raw_user['protected'] else user


# db = utils.db(name='melb-tweet', url='172.26.131.114:5984')
db = utils.db(url='45.88.195.224:9001')
udb = utils.db(name='users', url='45.88.195.224:9001')

with open('twitter.json', 'r') as f:
    for tweets in utils.split_every(gen(f), 1000):
        parsed_user = [parse_user(t['user']) for t in tweets]
        # parsed_tweets, parsed_user = [], []
        # for t in tweets:
        #     data = utils.parse_tweet(t)
        #     if data:
        #         parsed_tweets.append(data)
        #         parsed_user.append(parse_user(t['user']))
        # parsed_tweets = utils.bulk_parse_tweet(tweets)
        # parsed_user = [parse_user(t['user']) for t in tweets]
        # print(len(parsed_tweets), len(parsed_user))
        # break
        # result = db.update(parsed_tweets)
        result2 = udb.update(parsed_user)
        print(f'{len(tweets)}/{sum([r2[0] for r2 in result2])}')
        # print(
        #     f'Parse {len(parsed_tweets)}/{len(tweets)}  Upload {sum([r[0] for r in result])}/{sum([r2[0] for r2 in result2])}')

        # break
        
        # pprint(parsed_tweets)
        # break
