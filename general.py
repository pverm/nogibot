import requests
import pickle
import hashlib
import re
import os
from datetime import datetime, timedelta


def browser_get(url, **kwargs):
    # need to fake browser request else server responds with 403
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    r = requests.get(url, headers=headers, **kwargs)
    return r


def older_than_14_days(datestring):
    d = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ')
    return datetime.now() - timedelta(days=14) > d


def valid_name(name):
    """
    remove any invalid characters from folder/file name and cut to max 200 bytes

    :param name: folder or filename
    """
    stripped = re.sub(r'[/\\:*?"<>|]', '', name.strip())
    while len(stripped.encode('utf-8')) > 200:
        stripped = stripped[:-1]
    stripped = stripped.rstrip('.')  # remove dots at end of name
    stripped = stripped.rstrip(' ')  # remove blank space at end of name
    return stripped


def get_md5_hash(data):
    h = hashlib.md5()
    h.update(data)
    return h.hexdigest()


def load_blog_entries():
    if not os.path.exists('blog.p'):
        return dict()
    with open('blog.p', 'rb') as fin:
        return pickle.load(fin)


def save_blog_entries(blogs):
    with open('blog.p', 'wb') as fout:
        pickle.dump(blogs, fout)
