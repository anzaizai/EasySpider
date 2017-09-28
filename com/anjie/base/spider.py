from lxml.html import etree;

from com.anjie.mode.e_request import ERequest;


class BaseSpider:
    def __init__(self):
        super(BaseSpider, self).__init__();
        self.seed_url = None;
        self.seed_request = None;
        self.pipeline_item = None;
        self.requests = [];
        self.spiderName = "";

    def addRequest_urls(self, urls):
        if urls:
            for r in map(lambda url: ERequest(url, spiderName=self.spiderName), urls):
                self.requests.append(r);

    def pagerProcess(self, page):
        pass;

    def pagerBack(self, page, rq):

        try:
            if rq.needParse:
                page = etree.HTML(page);
        finally:
            self.pagerProcess(page);

        item = self.pipeline_item;
        requests = None;
        if len(self.requests) > 0:
            requests = self.requests.copy();

        return (self.pipeline_item, requests)

    # 返回种子请求
    def getSeeds(self):
        result = [];
        if self.seed_url:
            for url in self.seed_url:
                r = ERequest(url=url, spiderName=self.spiderName);
                r.headers = {}
                result.append(r);

        if self.seed_request:
            for rq in self.seed_request:
                if rq.headers is None:
                    rq.headers = {};
                result.append(rq)
        return result;
