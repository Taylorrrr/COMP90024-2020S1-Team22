import time
import ujson
from shapely.geometry import shape, point
from shapely import speedups
import couchdb
import utils


def get_zone(geo, zones):
    for z, s in zones.items():
        if s.contains(point.Point(geo)):
            return z
    return 'und'


def load_zones(file='SA2'):
    file = 'SA2'
    raw = ujson.load(open(f'../aurin/{file}.json'))
    return {zone['properties']['feature_code']: shape(
        zone['geometry']) for zone in raw['features']}


def add_zone(doc, zones):
    geo = doc['geo']
    doc['zone'] = get_zone(doc['geo'], zones)
    return doc


def main(chunk_size=500):

    db = utils.db(url='172.26.131.114:5984')
    mango = {
        'selector': {
            'geo': {'$exists': True},
            'zone': {'$exists': False}
        },
        'use_index': 'tweet-geo-index',
        # 'fields': ['_id', '_rev', 'geo'],
        'limit': chunk_size
    }

    zones = load_zones()
    while True:
        try:
            docs = [add_zone(doc, zones) for doc in db.find(mango)]
            if not docs:
                time.sleep(20)
            result = db.update(docs)
            print(f'{sum([r[0] for r in result])}/{len(docs)} updated.')
        except:
            time.sleep(5)



if __name__ == "__main__":
    main()