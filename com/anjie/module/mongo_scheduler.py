from urllib import parse;
from urllib.robotparser import RobotFileParser;

from com.anjie.base.scheduler import BaseScheduler
from com.anjie.mode.spider_exception import SpiderException;
from com.anjie.utils.elog import Elog
from com.anjie.utils.utils import UserAgent;
from com.anjie.mode.MongoQueue import MongoQueue;


class MongoScheduler(BaseScheduler):
    def __init__(self):
        super(MongoScheduler, self).__init__();

        # 待抓取队列
        self.mongo_queue = MongoQueue();

    def __iter__(self):
        return self

    def __next__(self):
        try:
            r = self.mongo_queue.pop();
        except KeyError as e:
             raise StopIteration
        else:
            return r;

    def nextRequest(self):
        try:
            r = self.mongo_queue.pop();
        except IndexError as e:
            return None;
        except KeyError as e:
            return None
        else:
            return r;

    def isNotEmpty(self):
        if self.mongo_queue and self.mongo_queue.peek():
            return True;
        else:
            return False;

    def addRequest(self, rq):
        rq.headers.setdefault(UserAgent.user_agent_key, UserAgent.user_agent_list[0]);
        self.mongo_queue.push(rq);

    def addRequests(self, rqs):
        for r in rqs:
            r.headers.setdefault(UserAgent.user_agent_key, UserAgent.user_agent_list[0]);
            self.mongo_queue.push(r);

    def addLoserRequest(self, rq):
        rq.headers.setdefault(UserAgent.user_agent_key, UserAgent.user_agent_list[0]);
        self.mongo_queue.push(rq);

    def addCompleteRequest(self, rq):
        self.mongo_queue.complete(rq.url);
