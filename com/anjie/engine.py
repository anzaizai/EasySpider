# Created by zaizai at 2017/9/21

from com.anjie.module.default_download import DefaultDownload;
from com.anjie.module.default_scheduler import DefaultScheduler;
from com.anjie.utils.elog import Elog;
from com.anjie.spider.myspider import Spider


class Engine:


    def __init__(self,spider = None,scheduler = DefaultScheduler(),download =DefaultDownload(),pipline=None ):
        super(Engine, self).__init__();
        self.spider = spider;
        self.scheduler = scheduler;
        self.download = download();
        self.pipline = pipline;

    def addSpider(self, spider):
        self.spider = spider;

    def start(self):
        self.scheduler.addRequests(self.spider.getSeeds())
        while True:
            rq = self.scheduler.nextRequest();
            if rq is None:
                Elog.warning('Engine is will stop,because scheduler has not more request be schedule');
                break;


            resultPage = self.download.excuteRequest(rq);


            if resultPage is not None:
                (pipelineItems, nextRequests) = self.spider.pagerBack(resultPage);
                if pipelineItems and self.pipline:
                    self.pipline.piplineData(pipelineItems);
                if nextRequests:
                    self.scheduler.addRequests(nextRequests);
            else:
                # 判断是否需要加入请求重新请求队列
                pass

    def sleep(self, time):
        pass;

    def stop(self):
        pass


if __name__ == '__main__':
    e = Engine();
    e.addSpider(Spider());
    e.start()