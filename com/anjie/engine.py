# Created by zaizai at 2017/9/21

from com.anjie.module.default_download import DefaultDownload;
from com.anjie.module.default_scheduler import DefaultScheduler;
from com.anjie.module.default_pipeline import DefaultPipeline;

from com.anjie.module.mongo_scheduler import MongoScheduler;
from com.anjie.utils.elog import Elog;
from com.anjie.spider.ThreadSpider import ThreadSpider;
from datetime import datetime
import threading, time
import multiprocessing
import asyncio
import functools
import psutil
from com.anjie.spider.AnJuKePipeline import AnJuKePipeline
from com.anjie.spider.AnJukeSpider import AnJuKeSpider;


class Engine:
    def __init__(self, spider=None, scheduler=MongoScheduler(), download=DefaultDownload(delay=5), pipline=None):
        super(Engine, self).__init__();

        self.spider = dict();
        if spider:
            for s in spider:
                self.spider.setdefault(s.spiderName, s);
        self.scheduler = scheduler;
        self.scheduler.mongo_queue.clear();
        self.download = download;
        self.pipeline = dict();
        if pipline:
            for p in pipline:
                self.pipeline.setdefault(p.belongToSpider, p);
        self.loop = asyncio.get_event_loop();
        self.max_number = 4;
        self.isSleep = False;
        self.isParseing = False;

    def addSpider(self, spider):
        self.spider.add(spider);

    def startLoop(self, loop):
        asyncio.set_event_loop(loop);
        loop.run_forever();

    # 协程下载页面
    async def download_task(self, rq):
        resultPage = self.download.excuteRequest(rq);
        if resultPage is not None:
            self.scheduler.mongo_queue.complete(rq.url);
        spider = self.spider.get(rq.spiderName, None)
        if spider:
            (pipelineItems, nextRequests) = spider.pagerBack(resultPage, rq);
        if nextRequests:
            self.scheduler.addRequests(nextRequests);

        pipeline = self.pipeline.get(rq.spiderName, None)
        if pipelineItems and pipeline:
            pipeline.piplineData(pipelineItems);
        return (resultPage, rq);


    def done_call_back(self, loop, result):
        print('done_call_back is Done.')
        # loop.stop();


    def parse_done_call_back(self, loop, result):
        print('parse_done_call_back is Done.')
        # loop.stop();
        self.isParseing = False;

    async def main_task(self, rqList):
        tasks = [];
        for rq in rqList:
            coroutine = self.download_task(rq);
            tasks.append(coroutine)
        return await asyncio.gather(*tasks)

    def getSeeds(self):

        rqs = list()

        print(self.spider)
        for k, s in self.spider.items():
            rqs.extend(s.getSeeds());
        return rqs;

    def start(self):
        try:
            self.scheduler.addRequests(self.getSeeds())
            Elog.info('>>start time is %s' % datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
            rqList = [];
            while True:
                if not self.scheduler.isNotEmpty() and not self.isParseing:
                    time.sleep(10);
                    if not self.scheduler.isNotEmpty() and not self.isParseing:
                        Elog.warning('Engine is will stop,because scheduler has not more request be schedule');
                        break;
                while self.scheduler.isNotEmpty():
                    rq = self.scheduler.nextRequest();
                    rqList.append(rq);
                    if len(rqList) < self.max_number:
                        continue;
                    else:
                        break
                if len(rqList) > 0:
                    coroutine = self.main_task(rqList);
                    task = asyncio.ensure_future(coroutine)
                    results = self.loop.run_until_complete(task);
                    rqList.clear();
                    Elog.info('loop is rqList size is %s' % len(rqList))

                    # for result in results:
                    #     print('Task ret: ', result)


        except KeyboardInterrupt as e:

            print(asyncio.Task.all_tasks())
            print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
            self.loop.stop()
            self.loop.run_forever()
        finally:
            Elog.info('loop is close')
            self.loop.close()


    def sleep(self, time):
        pass;


    def stop(self):
        pass


def running_tas(spiders=None, pipelines=None, scheduler=DefaultScheduler()):
    e = Engine(scheduler=scheduler, pipline=pipelines, spider=spiders);
    e.start()


processes = []


def process_crawler(spiders, pipelines, scheduler):
    Elog.info(".......")
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    Elog.info('Starting {} processes'.format(num_cpus));

    # pool.apply(func=running_tas)
    startTime = datetime.now();
    # pool.join();
    for i in range(num_cpus):
        p = multiprocessing.Process(target=running_tas, args=(spiders, pipelines, scheduler,))
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.daemon = True
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()
    Elog.info('>>end time is %s' % datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    endTime = datetime.now();
    Elog.info('cost time is %d' % (endTime - startTime).seconds);


def stop(pid):
    print('进程暂停  进程编号 %s ' % (pid))
    p = psutil.Process(pid)
    p.suspend()


def wake(pid):
    print('进程恢复  进程编号 %s ' % (pid))
    p = psutil.Process(pid)
    p.resume()


def process_crawler_pasue():
    for p in processes:
        stop(p.pid)


def process_crawler_wake():
    for p in processes:
        wake(p.pid)
    for p in processes:
        p = psutil.Process(p.pid)
        print(p.is_running())


if __name__ == '__main__':
    process_crawler(spiders=[AnJuKeSpider(), ], pipelines=[AnJuKePipeline(), ], scheduler=MongoScheduler())
