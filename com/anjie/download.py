from  urllib import request, error, response

# 默认的重试次数
DEFAULT_RETRIES = 1
DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 ';

class Download:
    # 重试次数
    num_retries = 0;
    # 代理
    user_agent = None;

    def __init__(self, num_retries=DEFAULT_RETRIES,user_agent=DEFAULT_AGENT,):
        self.num_retries = num_retries;
        self.user_agent = user_agent;


    def download(self,url):
        print('download url is %s' % url);
        html = None;
        try:
            rq = request.Request(url=url);
            rq.add_header('User-Agent',self.user_agent);
            rp = request.urlopen(rq);

            print('download over url is: %s' % rp.geturl())
            html = rp.read();
        except error.URLError as e:
            print('download  error :%s' % e.reason);
            html = None;

            if self.num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.download(url, self.num_retries - 1);
                pass;

        return html;


if __name__ == '__main__':
    d = Download();
    print(d.download('http://www.baidu.com'))
