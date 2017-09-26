# Created by zaizai at 2017/9/26
from datetime import datetime, timedelta;
from pymongo import MongoClient, errors;
from com.anjie.utils.elog import Elog;
from com.anjie.mode.e_request import ERequest;
import pickle
from bson.binary import Binary
import zlib;


class MongoQueue:
    # OUTSTANDING 未完成的,PROCESSING处理中,COMPLETE已完成
    OUTSTANDING, PROCESSING, COMPLETE = range(3);

    def __init__(self, client=None, timeout=300):
        super(MongoQueue, self).__init__();
        self.client = MongoClient() if client is None else client;
        self.db = self.client.cache;
        self.timeout = timeout;

    def __bool__(self):
        record = self.db.crawl_queue.find_one(
            {'status': {'$ne': self.COMPLETE}}
        );
        return True if record else False;

    def push(self, rq):
        try:
            self.db.crawl_queue.insert(
                {'_id': rq.url, 'request': Binary(zlib.compress(pickle.dumps(rq))), 'status': self.OUTSTANDING}
            )
        except errors.DuplicateKeyError as e:
            pass

    def pop(self):
        record = self.db.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.utcnow()}}
        )
        if record:
            return pickle.loads(zlib.decompress(record['request']));
        else:
            self.repair()
            raise KeyError()

    def peek(self):
        record = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if record:
            return pickle.loads(zlib.decompress(record['request']));

    def complete(self, url):
        self.db.crawl_queue.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        """Release stalled jobs
        """
        record = self.db.crawl_queue.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            Elog.info('Released:' + record['_id'])

    def clear(self):
        Elog.info('mongo queue be clear')
        self.db.crawl_queue.drop()
