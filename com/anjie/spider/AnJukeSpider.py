from com.anjie.base.spider import BaseSpider;
from com.anjie.spider.house import House;
import re;


# Created by zaizai at 2017/9/22


class AnJuKeSpider(BaseSpider):
    def __init__(self):
        super(AnJuKeSpider, self).__init__();
        self.spiderName = 'AnJuKe'
        self.seed_url= ['https://gz.zu.anjuke.com/fangyuan/1090022909']
        # self.seed_url = ['https://gz.zu.anjuke.com/?from=navigation'];
        compileUrl = 'https://gz.zu.anjuke.com/fangyuan/\d+.*'
        self.detailPageCp = re.compile(compileUrl, re.IGNORECASE);
        compileTime = '.*：(\d+年\d+月\d+日)'
        self.timeCp = re.compile(compileTime,re.IGNORECASE)

    def pagerProcess(self, url, page):

        result = self.detailPageCp.match(url);
        if result:
            print('详情页：%s' % url)
            title = page.xpath('//div[@id="content"]//h3[@class="fl"]/text()')
            print('>>>>title is %s' % title)
            box1 = page.xpath('//div[@id="content"]//div[@class="box"]/div//dl')
            print(box1)
            print(box1[0].xpath('./dt/text()'))
            print(box1[0].xpath('./dd/strong/span/text()'))
            print(box1[0].xpath('./dd/strong/text()'))

            print(box1[1].xpath('./dt/text()'))
            print(box1[1].xpath('./dd/text()'))

            print(box1[2].xpath('./dt/text()'))
            print(box1[2].xpath('./dd/text()'))

            print(box1[3].xpath('./dt/text()'))
            print(box1[3].xpath('./dd/text()'))

            print(box1[4].xpath('./dt/text()'))
            print(box1[4].xpath('./dd/a/text()'))

            print(box1[5].xpath('./dt/text()'))
            print(box1[5].xpath('./dd/a/text()'))

            print(box1[7].xpath('./dt/text()'))
            print(box1[7].xpath('./dd/text()'))

            print(box1[8].xpath('./dt/text()'))
            print(box1[8].xpath('./dd/text()'))

            print(box1[9].xpath('./dt/text()'))
            print(box1[9].xpath('./dd/text()'))

            print(box1[10].xpath('./dt/text()'))
            print(box1[10].xpath('./dd/text()'))

            print(box1[11].xpath('./dt/text()'))
            print(box1[11].xpath('./dd/text()'))

            configuration = page.xpath('//div[@id="content"]//div[@id="proLinks"]/p/span/text()')
            print(configuration)

            description = page.xpath('//div[@id="content"]//div[@id="propContent"]/div/span/text()')

            print(description)


            publishTime = page.xpath('//div[@id="content"]//div[@class="text-mute extra-info"]/text()')
            reuslt = self.timeCp.match(publishTime[0]);
            print(reuslt.groups())


            # 小区信息
            property = page.xpath('//*[@id="commmap"]//dl')
            print(property[6].xpath('./dt/text()'))
            print(property[6].xpath('./dd/text()'))
            print(property[7].xpath('./dt/text()'))
            print(property[7].xpath('./dd/text()'))
            print(property[8].xpath('./dt/text()'))
            print(property[8].xpath('./dd/text()'))
            print(property[9].xpath('./dt/text()'))
            print(property[9].xpath('./dd/text()'))
            print(property[12].xpath('./dt/text()'))
            print(property[12].xpath('./dd/text()'))


            # 人员信息
            username = page.xpath('//*[@id="broker_true_name"]/text()')
            print(username)
            phone = page.xpath('//p[@class="broker-mobile"]/text()')

            phone = phone[0].replace(' ', '')
            print(phone)
            company = page.xpath('//div[@class="broker-company"]//a/text()')
            print(company)

        else:
            print('其他页：%s' % url)
            next_link = [];
            list_result = page.xpath('//div[@class="maincontent"]//div[@class="zu-itemmod  "]')
            house_list = [];
            house = None;
            result_list = [];
            next_link = [];
            for node in list_result:
                # h = House();
                # print(etree.tostring(node,encoding="utf-8",pretty_print=True,method="html").decode())
                # 抽取
                # title = node.xpath('.//div[@class="zu-info"]/h3/a/text()');
                # h.title = title;
                # 抽取链接
                url = node.xpath('.//div[@class="zu-info"]/h3/a/@href')
                if url:
                    next_link.extend(url)
                # h.url = url;
                # temp = node.xpath('.//div[@class="zu-info"]/p[1]/text()')
                # (house_type, sale_type, level, floor_number) = temp;
                # h.house_type = house_type;
                # h.sale_type = sale_type;
                # h.level = level;
                # h.floor_number = floor_number;
                # # 抽取地址
                # area_name = node.xpath('.//div[@class="zu-info"]/address/a/text()')
                # h.area_name = area_name;
                # area = node.xpath('.//div[@class="zu-info"]/address/text()')
                # for ele in area:
                #     if len(ele.strip()) > 0:
                #         area = ele.strip();
                #         break;
                # h.addr = area;
                # # 抽取联系人
                # user = node.xpath('.//div[@class="zu-info"]/p[2]/span/text()')
                # h.user = user;
                # supplement = node.xpath('.//div[@class="zu-info"]/p[2]/em/text()')
                # h.supplement = supplement;
                #
                # # 获取价格
                # price = node.xpath('.//div[@class="zu-side"]//strong/text()')
                #
                # h.price = price;
                # unit = node.xpath('.//div[@class="zu-side"]/p/text()')
                # h.unit = unit;
                # result_list.append(h);

            # links = page.xpath('//*[@class="multi-page"]/a/@href');
            # # 利用集合过滤重复的链接
            # s = set(links)
            #
            # next_link = list(s);
            #
            print('抽取的链接:%s' % next_link)
            self.pipeline_item = result_list;
            self.addRequest_urls(next_link);


if __name__ == '__main__':
    compileUrl = 'https://gz.zu.anjuke.com/fangyuan/\d+.*'
    cp = re.compile(compileUrl, re.IGNORECASE);
    reuslt = cp.match('https://gz.zu.anjuke.com/fangyuan/p376e2376487326/')
    print(dir(reuslt))
    print(reuslt)
    #  print(reuslt.group())
    #    print(reuslt.groups())
