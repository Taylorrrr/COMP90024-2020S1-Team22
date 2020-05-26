import utils
from pprint import pprint
import sys
from concurrent.futures import ThreadPoolExecutor


def validate(n):
    try:
        valid = 'rate_limit_context' in utils.api(n).rate_limit_status()
        # print(f'Token {n: 2} is valid')
    except Exception:
        token = utils.credential[n]
        print(f'Token {n: 2} {token["consumer_key"]} is invalid')


def limit(keyword, n):
    def helper(json):
        if isinstance(json, dict):
            for k, v in json.items():
                if keyword in k:
                    print(f'Key {n:3}  {k}: {v["remaining"]}/{v["limit"]}')
                else:
                    helper(v)
        elif isinstance(json, list):
            for item in json:
                helper(item)

    api = utils.api(n)
    status = api.rate_limit_status()
    helper(status)


count = len(utils.credential)
if len(sys.argv) == 1:
    try:
        with ThreadPoolExecutor(max_workers=72) as executor:
            executor.map(validate, range(count))
    except Exception as e:
        print(repr(e))
else:
    arg1 = sys.argv[1]
    if arg1.isdigit():
        if len(sys.argv) == 2:
            pprint(utils.api(int(arg1)).rate_limit_status())
        else:
            limit(sys.argv[2], int(arg1))
    else:
        with ThreadPoolExecutor(max_workers=72) as executor:
            executor.map(limit, [arg1]*count, range(count))
