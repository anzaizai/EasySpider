from lxml.html import etree;

from com.anjie.mode.e_request import ERequest;


class BaseSpider:
    def __init__(self):
        super(BaseSpider, self).__init__();
        self.seed_url = None;
        self.pipeline_item = None;
        self.requests = [];


    def addRequest_urls(self, urls):
        if urls:
            for r in map(lambda url:ERequest(url), urls):
                self.requests.append(r);

    def pagerProcess(self, page):
        pass;

    def pagerBack(self, html):
        page = root = etree.HTML(html);
        self.pagerProcess(page);
        item = self.pipeline_item;
        requests = None;
        if len(self.requests) > 0:
            requests = self.requests.copy();

        return (self.pipeline_item, requests)

    # 返回种子请求
    def getSeeds(self):
        result = [];
        for url in self.seed_url:
            r = ERequest(url=url);
            result.append(r);
        return result;
