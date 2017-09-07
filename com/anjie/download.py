from  urllib import request, error, response
def download(url, num_retries=2):
    print('download url is %s' % url);
    html = None;
    try:
        rq = request.Request(url=url);
        rp = request.urlopen(rq);
        print(dir(rp))
        print('download over url is: %s'%rp.geturl())
        # print('response code is %d' % r.code);
        html = rp.read();
    except error.URLError as e:
        print('download  error :%s' % e.reason);
        html = None;
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                return download(url, num_retries - 1);
            pass;

    return html;


if __name__ == '__main__':
    print(download('http://www.baidu.com',2))