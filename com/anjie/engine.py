# Created by zaizai at 2017/9/21

from com.anjie.module.default_download import DefaultDownload;
from com.anjie.module.default_scheduler import DefaultScheduler;
from com.anjie.module.mongo_scheduler import MongoScheduler;
from com.anjie.utils.elog import Elog;
from com.anjie.spider.myspider import Spider
from com.anjie.spider.ThreadSpider import ThreadSpider;
from datetime import datetime
import threading, time
import multiprocessing


class Engine:
    def __init__(self, spider=None, scheduler=MongoScheduler(), download=DefaultDownload(delay=0), pipline=None):
        super(Engine, self).__init__();
        self.spider = spider;
        self.scheduler = scheduler;
        self.scheduler.mongo_queue.clear();
        self.download = download;
        self.pipline = pipline;

    def addSpider(self, spider):
        self.spider = spider;

    def start(self):
        self.scheduler.addRequests(self.spider.getSeeds())
        Elog.info('>>start time is %s' % datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

        self.thread_task()

    def thread_task(self):
        while True:
            rq = self.scheduler.nextRequest();
            if rq is None:
                Elog.warning('Engine is will stop,because scheduler has not more request be schedule');
                break;

            threads = []
            max_threads = 8;
            lock = threading.Lock();
            while threads or self.scheduler.isNotEmpty():
                # the crawl is still active
                for thread in threads:
                    if not thread.is_alive():
                        # remove the stopped threads
                        threads.remove(thread)
                while len(threads) < max_threads and self.scheduler.isNotEmpty():
                    # can start some more threads

                    try:
                        lock.acquire();
                        rp = self.scheduler.nextRequest();
                        thread = ThreadTask(rq=rq, download=self.download, spider=self.spider)
                        thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
                        thread.start()
                        threads.append(thread)
                    except Exception:
                        pass
                    finally:
                        lock.release();

                        # all threads have been processed
                        # sleep temporarily so CPU can focus execution on other threads


    def sleep(self, time):
        pass;

    def stop(self):
        pass


class ThreadTask(threading.Thread):
    def __init__(self, rq, download, pipline=None, scheduler=None, spider=None):
        super(ThreadTask, self).__init__();
        self.rq = rq;
        self.download = download;
        self.pipline = pipline;
        self.scheduler = scheduler;
        self.spider = spider;

    def run(self):
        resultPage = self.download.excuteRequest(self.rq);
        if resultPage is not None:
            (pipelineItems, nextRequests) = self.spider.pagerBack(resultPage, self.rq);
            if pipelineItems and self.pipline:
                self.pipline.piplineData(pipelineItems);
            if nextRequests:
                self.scheduler.addRequests(nextRequests);
        else:
            # 判断是否需要加入请求重新请求队列
            pass


def running_tas():
    e = Engine(scheduler=MongoScheduler());
    e.addSpider(ThreadSpider());
    e.start()


def process_crawler():
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    Elog.info('Starting {} processes'.format(num_cpus));
    processes = []
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
