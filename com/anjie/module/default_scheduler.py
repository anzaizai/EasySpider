from urllib import parse;
from urllib.robotparser import RobotFileParser;

from com.anjie.base.scheduler import BaseScheduler
from com.anjie.mode.spider_exception import SpiderException;
from com.anjie.utils.elog import Elog
from com.anjie.utils.utils import UserAgent;



class DefaultScheduler(BaseScheduler):
    def __init__(self):
        super(DefaultScheduler, self).__init__();

        # 待抓取队列
        self.belle_queue = list();

        # 下载失败队列
        self.loser_queue = [];

        # robots数据缓存
        self.rp_cache_queue = [];

        # robots禁止队列
        self.robots_loser_queue = []

        # 已爬取url
        self.crawl_over_queue = [];

        self.rp_cache = dict();

    def __iter__(self):
        return self

    def __next__(self):
        r = self.belle_queue.pop();
        if r is None:
            raise StopIteration
        else:
            return r;

    def nextRequest(self):
        try:
            r = self.belle_queue.pop();
        except IndexError as e:
            return None;
        else:
            return r;

    def isNotEmpty(self):
        if self.belle_queue and len(self.belle_queue)>0:
            return True;
        else:
            return False;


    def addRequest(self, rq):
        rq.headers.setdefault(UserAgent.user_agent_key, UserAgent.user_agent_list[0]);
        self.belle_queue.extend(rq);

    def addRequests(self, rqs):
        for r in rqs:
            r.headers.setdefault(UserAgent.user_agent_key, UserAgent.user_agent_list[0]);
            self.belle_queue.append(r);

    def addLoserRequest(self, rq):
        rq.headers.setdefault(UserAgent.user_agent_key, UserAgent.user_agent_list[0]);
        self.belle_queue.extend(rq);

    def start_craw(self):
        if not self.spider:
            raise SpiderException("spider obeject is None")

        if not hasattr(self.spider, 'start_url'):
            raise SpiderException("spider must have an start_url attribute")

        if not hasattr(self.spider, 'pager_back'):
            raise SpiderException("spider must have an pager_back method")

        self.crawl_queue.extend(self.spider.start_url);
        # 初始化每个url请求的次数为0

        while self.crawl_queue:
            url = self.crawl_queue.pop();

            html = None;
            # 咱要做一只优雅的爬虫
            rp = self.get_robots(url);

            if rp is not None:
                if rp.can_fetch(useragent=self.download.user_agent, url=url):
                    html = self.download.download(url=url);
                else:
                    Elog.warning(
                        'current url : %s and user_agent: %s is be disallow for robots.txt' % (url, self.user_agent))
                    html = None;

            if html:
                self.crawl_over_queue.append(url);

            pipeline_item = self.spider.pager_back(url, html);
            # 判断是否有增加请求url
            print(pipeline_item)
            if self.pipline and pipeline_item and pipeline_item['item']:
                self.pipline.piplineData(pipeline_item['item']);

            if pipeline_item['url']:
                for r in pipeline_item['url']:
                    if not r in self.crawl_over_queue and r not in self.crawl_queue:
                        self.crawl_queue.append(r);


                        # 解析robots.txt文件

    def get_robots(self, url):

        """Initialize robots parser for this domain
        """
        (proto, rest) = parse.splittype(url)
        # 获取域名res
        res, rest = parse.splithost(rest)
        rp = None;
        try:
            rp = self.rp_cache[res];
        except KeyError as e:
            Elog.error('key error');
            pass;
        else:
            return rp;

        rp = RobotFileParser()
        rp.set_url(parse.urljoin(url, '/robots.txt'))
        rp.read()

        if self.rp_cache is not None:
            if rest:
                self.rp_cache[res] = rp;
            else:
                Elog.info('url:%s 解析域名失败' % url);

        return rp
