from datetime import datetime, timedelta
from  pymongo import MongoClient
import pickle
from bson.binary import Binary
import zlib;
from com.anjie.utils.elog import Elog


# 启动指令 mongodb -dbpath .
class MongoCache:
    expires = None;
    client = None;
    db = None;

    def __init__(self, expires=timedelta(seconds=60)):
        try:
            self.client = MongoClient('localhost', 27017) if self.client is None else self.client;
            self.db = self.client.cache;
            self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds());
        except:
            pass

    def __setitem__(self, key, value):
        Elog.info('设置缓存 url:%s' % key)
        record = {'result': Binary(zlib.compress(pickle.dumps(value))), 'timestamp': datetime.utcnow()};
        self.db.webpage.update({'_id': key}, {'$set': record}, upsert=True);

    def __getitem__(self, item):
        Elog.info('取缓存 url:%s' % item)

        record = self.db.webpage.find_one({'_id': item})
        if record:
            return pickle.loads(zlib.decompress(record['result']));
        else:
            raise KeyError('url=%s does not exist');
