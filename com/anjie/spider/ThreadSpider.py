# Created by zaizai at 2017/9/25

from  com.anjie.base.spider import BaseSpider;
from com.anjie.mode.e_request import ERequest;
import  csv
import os;


class ThreadSpider(BaseSpider):
    def __init__(self):
        super(ThreadSpider, self).__init__();
        self.max_urls = 000;
        ulist = 'https://www.baidu.com/';
        rlist = [];
        for i in range(0,100):
            r = ERequest(url=ulist+str(i), needParse=False)
            rlist.append(r);
        self.seed_request = list(rlist)

        # with open('top-1m.csv','r') as fp:
        #     reader = csv.reader(fp)
        #
        #     for _,website in reader:
        #         website = 'http://' + website;
        #
        #         if len(rlist) == self.max_urls:
        #             break;




    def pagerProcess(self, page):
        print(page)
        # if url == self.seed_url:
        #     urls = []
        #     cache = MongoCache()
        #     with ZipFile(StringIO(html)) as zf:
        #         csv_filename = zf.namelist()[0]
        #         for _, website in csv.reader(zf.open(csv_filename)):
        #             if 'http://' + website not in cache:
        #                 urls.append('http://' + website)
        #                 if len(urls) == self.max_urls:
        #                     break
        #     return urls
        self.pipeline_item=['sadasdsad']




