import utils
from concurrent.futures import ThreadPoolExecutor

# db = utils.db(url='45.88.195.224:9001')
db = utils.db(name='users',url='45.88.195.224:9001')


def delete(n):
    rows = db.view('user_tree/searched',
                   startkey=[True, 1], endkey=[True, 1, {}], reduce=False, skip=n*100, limit=100, include_docs=True)
    # ids = [row.id for row in rows]
    docs = [row.doc for row in rows]

    for doc in docs:
        doc['searched'] = False

    result = db.update(docs)
    print(f'update {sum([r[0] for r in result])}/{len(docs)}')


rows = db.view('tree/searched', startkey=['que'], endkey=[{}, {}], reduce=False).rows
    # break
ids = [r.id for r in rows]
print(len(ids))
utils.bulk_update_by_id(db, ids, searched=False)
