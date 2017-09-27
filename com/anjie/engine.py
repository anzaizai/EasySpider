# Created by zaizai at 2017/9/21

from com.anjie.module.default_download import DefaultDownload;
from com.anjie.module.default_scheduler import DefaultScheduler;
from com.anjie.module.default_pipeline import DefaultPipeline;

from com.anjie.module.mongo_scheduler import MongoScheduler;
from com.anjie.utils.elog import Elog;
from com.anjie.spider.myspider import Spider
from com.anjie.spider.ThreadSpider import ThreadSpider;
from datetime import datetime
import threading, time
import multiprocessing
import asyncio
import functools


class Engine:
    def __init__(self, spider=None, scheduler=MongoScheduler(), download=DefaultDownload(delay=0), pipline=None):
        super(Engine, self).__init__();
        self.spider = spider;
        self.scheduler = scheduler;
        self.scheduler.mongo_queue.clear();
        self.download = download;
        self.pipline = pipline;
        self.loop = asyncio.get_event_loop();

        self.pageConsumer = self.pageConsumer();
        self.pageConsumer.send(None);

    def addSpider(self, spider):
        self.spider = spider;

    def startLoop(self, loop):
        asyncio.set_event_loop(loop);
        loop.run_forever();

    # 协程下载页面
    async def download_task(self, pageConsumer, rq):
        resultPage = self.download.excuteRequest(rq);
        if resultPage is not None:
            pageConsumer.send((resultPage, rq))
        return (resultPage, rq);

    def done_call_back(self, loop, result):
        print('done_call_back is Done.')
        # loop.stop();

    def parse_done_call_back(self, loop, result):
        print('parse_done_call_back is Done.')
        # loop.stop();

    async def main_task(self, rqList):
        tasks = [];
        for rq in rqList:
            coroutine = self.download_task(self.pageConsumer, rq);
            tasks.append(coroutine)
        return await asyncio.gather(*tasks)



    def start(self):
        try:
            self.scheduler.addRequests(self.spider.getSeeds())
            Elog.info('>>start time is %s' % datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
            max_number = 4;
            rqList = [];
            while True:
                if not self.scheduler.isNotEmpty():
                    Elog.warning('Engine is will stop,because scheduler has not more request be schedule');
                    break;
                while self.scheduler.isNotEmpty():
                    rq = self.scheduler.nextRequest();
                    rqList.append(rq);
                    if len(rqList) < max_number:
                        continue;
                if len(rqList) > 0:
                    coroutine = self.main_task(rqList);
                    task = asyncio.ensure_future(coroutine)
                    results = self.loop.run_until_complete(task);
                    for result in results:
                        print('Task ret: ', result)
                    rqList.clear();

        except KeyboardInterrupt as e:
            print(asyncio.Task.all_tasks())
            print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
            self.loop.stop()
            self.loop.run_forever()
        finally:
            self.loop.close()

    def sleep(self, time):
        pass;

    def stop(self):
        pass

    async def parse_task(self, resultPage, rq):
        (pipelineItems, nextRequests) = self.spider.pagerBack(resultPage, rq);
        if pipelineItems and self.pipline:
            self.pipline.piplineData(pipelineItems);
        if nextRequests:
            self.scheduler.addRequests(nextRequests);

    def pageConsumer(self):
        while True:
            (resultPage, rq) = yield
            print('pageConsumer')

            if resultPage is not None:
                coroutine = self.parse_task(resultPage, rq);
                task = asyncio.ensure_future(coroutine)
                task.add_done_callback(functools.partial(self.parse_done_call_back, self.loop))
                # self.loop.run_until_complete(task)

            else:
                # 判断是否需要加入请求重新请求队列
                pass


def running_tas():
    e = Engine(scheduler=MongoScheduler(), pipline=DefaultPipeline());
    e.addSpider(ThreadSpider());
    e.start()


def process_crawler():
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    Elog.info('Starting {} processes'.format(num_cpus));
    processes = []
    num_cpus = 1;
    startTime = datetime.now();
    for i in range(num_cpus):
        p = multiprocessing.Process(target=running_tas, )
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()
    Elog.info('>>end time is %s' % datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    endTime = datetime.now();
    Elog.info('cost time is %d' % (endTime - startTime).seconds);


if __name__ == '__main__':
    process_crawler()
