# Created by zaizai at 2017/9/21


# 默认的代理
DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 '


class ERequest:
    def __init__(self, url=None, headers={}, needParse=True, spiderName=''):
        super(ERequest, self).__init__();
        self.url = url;
        self.headers = headers;
        self.needParse = needParse;
        self.spiderName = spiderName;
