import random;
from  urllib import request, error

from com.anjie.base.download import BaseDownload;
from  com.anjie.utils.elog import Elog
from com.anjie.utils.throttle import Throttle;
import threading

# 默认的延迟事件
DEFAULT_DELAY = 5
# 默认的重试次数
DEFAULT_RETRIES = 1
# 默认的超时事件
DEFAULT_TIMEOUT = 60


class DefaultDownload(BaseDownload):
    def __init__(self, num_retries=DEFAULT_RETRIES, cache=None, proxies=None,
                 delay=DEFAULT_DELAY):
        super(DefaultDownload, self).__init__();
        # 重试次数
        self.num_retries = num_retries;
        # 代理
        # 缓存
        self.cache = cache;
        self.proxies = proxies;
        self.throttle = Throttle(delay)

    def excuteRequest(self, rq):
        return self.download(rq)

    def download(self, rq):
        Elog.info('download url is %s' % rq.url);
        result = None;
        if self.cache is not None:
            try:
                result = self.cache[rq.url];
            except KeyError as e:
                Elog.warning('url %s is available in cache' % rq.url)
                pass;
            else:
                # 没有异常时执行这里
                if result is not None and self.num_retries > 0 and 500 <= result['code'] < 600:
                    # 上次请求时没有拿到数据
                    Elog.info("server error so ignore result from cache of url %s and re-download" % rq.url);
                    result = None;

        # 没有配置cache获取cache未缓存该url数据则走这里
        if result is not None:
            return result['html'];

        if result is None:
            Elog.info("url %s is haven't cache, so still need to download");
            # proxy = random.choice(self.proxies) if self.proxies else None
            proxy = None;
            if self.proxies is not None:
                proxy = random.choice(self.proxies);
            result = self.realDownload(rq, proxy=proxy,
                                       num_retries=self.num_retries);
        if self.cache is not None:
            # save data to cache
            self.cache[rq.url] = result;
        return result['html'];

    def realDownload(self, rq, proxy, num_retries, data=None):
        Elog.info('realDownload url is %s' % rq.url);

        # 进行延迟请求
        self.throttle.wait(rq.url)

        html = None;
        code = None;
        try:
            rq = request.Request(url=rq.url, headers=rq.headers);
            rp = request.urlopen(rq);
            Elog.info('download over url is: %s' % rp.geturl())
            html = rp.read();
            code = rp.code;
        except error.URLError as e:
            Elog.error('download  error :%s' % e.reason);
            html = '';
            if self.num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.realDownload(rq, proxy, num_retries - 1);
                pass;
        except ConnectionResetError as e:
            Elog.error('ConnectionResetError  error');

        return {'html': html, 'code': code};


if __name__ == '__main__':
    d = DefaultDownload();
    print(d.download('http://www.baidu.com'))
