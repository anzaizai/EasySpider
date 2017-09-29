from com.anjie.base.spider import BaseSpider;
from com.anjie.spider.house import House;
import re;


# Created by zaizai at 2017/9/22


class TC58Spider(BaseSpider):
    def __init__(self):
        super(TC58Spider, self).__init__();
        self.spiderName = 'TC58Spider';
        # self.seed_url= ['http://gz.58.com/zufang/31309318967487x.shtml?entinfo=31309318967487_0&fzbref=0&from=1-list-0&params=busitime%5Edesc&psid=179071954197470652399624544&iuType=gz_2&ClickID=2&cookie=%7C%7C%7Cc5/njVl//1M1TjSDA2QUAg==&PGTID=0d3090a7-0000-34af-c049-a30de25ba462&local=3&apptype=0&key=&pubid=18587762&trackkey=31309318967487_6b6591c6-ba5d-46b5-bd4a-bede3bb6f930_20170928145224_1506581544297&fcinfotype=gz']
        self.seed_url = ['http://gz.58.com/chuzu/pn1/'];
        compileUrl = '.*://gz.58.com/chuzu/pn\d+.*'
        self.detailPageCp = re.compile(compileUrl, re.IGNORECASE);
        compileTime = '.*：(\d+年\d+月\d+日)'
        self.timeCp = re.compile(compileTime, re.IGNORECASE)

    def pagerProcess(self, url, page):

        result = self.detailPageCp.match(url);
        if not result:
            print('详情页：%s' % url)
            title = page.xpath('//div[@class="main-wrap"]//div[@class="house-title"]//h1/text()')
            print('>>>>title is %s' % title)
            price = page.xpath('//div[@class="main-wrap"]//div[@class="house-basic-desc"]//b[@class="f36"]/text()')
            print('>>>>title is %s' % price)

            price = page.xpath('//div[@class="main-wrap"]//div[@class="house-basic-desc"]//span[@class="c_ff552e"]/text()')
            print('>>>>title is %s' % price)
            price = page.xpath(
                '//div[@class="main-wrap"]//div[@class="house-basic-desc"]//span[@class="c_333"]/text()')
            print('>>>>title is %s' % price)

            price = page.xpath(
                '//*[@class="house-chat-txt"]/text()')
            print('>>>>title is %s' % price)

            price = page.xpath(
                '//a[@title="点击查看ta的信用"]/text()')
            print('>>>>title is %s' % price)

            price = page.xpath(
                '//p[@class="house-update-info c_888 f12"]/text()')
            print('>>>>title is %s' % price)



            nodes = page.xpath(
                '//div[@class="main-wrap"]//div[@class="house-basic-desc"]//ul/li')

            print(nodes[0].xpath('./span/text()'))
            print(nodes[1].xpath('./span/text()'))
            print(nodes[2].xpath('./span/text()'))
            print(nodes[3].xpath('./span[1]/text()'))
            print(nodes[3].xpath('./span/a/text()'))

            print(nodes[4].xpath('./span[1]/text()'))
            print(nodes[4].xpath('./span/a/text()'))
            print(nodes[5].xpath('./span/text()'))

            #房子详情描述
            nodes = page.xpath(
                '//div[@class="house-detail-desc"]//ul[@class="house-disposal"]/li/text()')

            print(nodes)
            nodes = page.xpath(
                '//div[@class="house-detail-desc"]//ul[@class="introduce-item"]/li/span[@class="a2"]/p/text()')

            print(nodes)

            nodes = page.xpath(
                '//a[@class="c_888 ab"]/em/text()')
            print(nodes)
            # box1 = page.xpath('//div[@id="content"]//div[@class="box"]/div//dl')
            # print(box1)
            # print(box1[0].xpath('./dt/text()'))
            # print(box1[0].xpath('./dd/strong/span/text()'))
            # print(box1[0].xpath('./dd/strong/text()'))
            #
            # print(box1[1].xpath('./dt/text()'))
            # print(box1[1].xpath('./dd/text()'))
            #
            # print(box1[2].xpath('./dt/text()'))
            # print(box1[2].xpath('./dd/text()'))
            #
            # print(box1[3].xpath('./dt/text()'))
            # print(box1[3].xpath('./dd/text()'))
            #
            # print(box1[4].xpath('./dt/text()'))
            # print(box1[4].xpath('./dd/a/text()'))
            #
            # print(box1[5].xpath('./dt/text()'))
            # print(box1[5].xpath('./dd/a/text()'))
            #
            # print(box1[7].xpath('./dt/text()'))
            # print(box1[7].xpath('./dd/text()'))
            #
            # print(box1[8].xpath('./dt/text()'))
            # print(box1[8].xpath('./dd/text()'))
            #
            # print(box1[9].xpath('./dt/text()'))
            # print(box1[9].xpath('./dd/text()'))
            #
            # print(box1[10].xpath('./dt/text()'))
            # print(box1[10].xpath('./dd/text()'))
            #
            # print(box1[11].xpath('./dt/text()'))
            # print(box1[11].xpath('./dd/text()'))
            #
            # configuration = page.xpath('//div[@id="content"]//div[@id="proLinks"]/p/span/text()')
            # print(configuration)
            #
            # description = page.xpath('//div[@id="content"]//div[@id="propContent"]/div/span/text()')
            #
            # print(description)
            #
            # publishTime = page.xpath('//div[@id="content"]//div[@class="text-mute extra-info"]/text()')
            # reuslt = self.timeCp.match(publishTime[0]);
            # print(reuslt.groups())
            #
            # # 小区信息
            # property = page.xpath('//*[@id="commmap"]//dl')
            # print(property[6].xpath('./dt/text()'))
            # print(property[6].xpath('./dd/text()'))
            # print(property[7].xpath('./dt/text()'))
            # print(property[7].xpath('./dd/text()'))
            # print(property[8].xpath('./dt/text()'))
            # print(property[8].xpath('./dd/text()'))
            # print(property[9].xpath('./dt/text()'))
            # print(property[9].xpath('./dd/text()'))
            # print(property[12].xpath('./dt/text()'))
            # print(property[12].xpath('./dd/text()'))
            #
            # # 人员信息
            # username = page.xpath('//*[@id="broker_true_name"]/text()')
            # print(username)
            # phone = page.xpath('//p[@class="broker-mobile"]/text()')
            #
            # phone = phone[0].replace(' ', '')
            # print(phone)
            # company = page.xpath('//div[@class="broker-company"]//a/text()')
            # print(company)






        else:
            print('其他页：%s' % url)
            next_link = [];
            list_result = page.xpath('//div[@class="content"]//ul[@class="listUl"]/li');
            house_list = [];
            house = None;
            result_list = [];
            for node in list_result:
                # h = House();
                # print(etree.tostring(node,encoding="utf-8",pretty_print=True,method="html").decode())
                # 抽取
                # title = node.xpath('.//div[@class="zu-info"]/h3/a/text()');
                # h.title = title;
                # 抽取链接
                url = node.xpath('.//div[@class="des"]/h2[1]/a/@href')
                if url:
                    next_link.extend(url)

            print('抽取的链接:%s' % next_link)
            self.pipeline_item = result_list;
            self.addRequest_urls(next_link);



