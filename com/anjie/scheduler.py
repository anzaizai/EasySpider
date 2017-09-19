from com.anjie.download import Download;
from com.anjie.spider_exception import SpiderException;
from com.anjie.pipeline import Pipeline;

class Scheduler:
    # 待抓取队列
    crawl_queue = [];
    #已爬取url
    crawl_over_queue = [];
    download = None;
    spider = None;
    pipline = None;

    def __init__(self, download=None, spider=None,pipline=None):
        self.download = download;
        self.spider = spider;
        self.pipline = pipline;
        pass;

    # 调用该函数开始让爬虫开始工作
    def start_craw(self):
        if not self.spider:
            raise SpiderException("spider obeject is None")

        if not hasattr(self.spider, 'start_url'):
            raise SpiderException("spider must have an start_url attribute")

        if not hasattr(self.spider, 'pager_back'):
            raise SpiderException("spider must have an pager_back method")

        self.crawl_queue.extend(self.spider.start_url);

        while self.crawl_queue:
            url = self.crawl_queue.pop();
            html = self.download.download(url=url);
            if  html:
                self.crawl_over_queue.append(url);

            pipeline_item = self.spider.pager_back(url, html);
            #判断是否有增加请求url
            print(pipeline_item)
            if self.pipline and pipeline_item and pipeline_item['item']:
                self.pipline.piplineData(pipeline_item['item']);

            if pipeline_item['url']:
                for r in pipeline_item['url']:
                    if not r in self.crawl_over_queue and r not  in self.crawl_queue:
                        self.crawl_queue.append(r);



