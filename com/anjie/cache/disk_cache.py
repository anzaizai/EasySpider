import os
import pickle
import re;
import zlib
from datetime import datetime, timedelta
from urllib import parse


class DiskCache:
    cache_dir = None;
    max_length = None;
    expires = None;

    def __init__(self, cache_dir='cache_dir', expires=timedelta(seconds=60 * 1)):
        self.cache_dir = cache_dir;
        self.expires = expires;

    def url_to_path(self, url):
        # create file system path for url
        components = parse.urlsplit(url=url);
        print(components.path)
        path = components.path;
        if path is None:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        fileName = components.netloc + path + components.query;
        # 替换非法字符，替换非0～9a~zA~Z-.,;_的字符为_
        fileName = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', fileName)
        # 控制每个字符最长取其前255个
        fileName = '/'.join(segment[0:255] for segment in fileName.split('/'));
        return os.path.join(self.cache_dir, fileName);

    def __getitem__(self, item):
        path = self.url_to_path(item);
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                result, timestamp = pickle.loads(zlib.decompress(fp.read()));
                if self.has_expired(timestamp):
                    raise KeyError('url=%s is has expired' % item);
                return result;
        else:
            raise KeyError(item + 'is not exists')

    def __setitem__(self, key, value):
        path = self.url_to_path(key);
        folder = os.path.dirname(path);
        if not os.path.exists(folder):
            os.makedirs(folder);

        timestamp = datetime.utcnow()
        data = pickle.dumps((value, timestamp))
        with open(path, 'wb') as fp:
            fp.write(zlib.compress(data));

    def has_expired(self, timestamp):
        return datetime.utcnow() > timestamp + self.expires
