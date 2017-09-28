from com.anjie.base.spider import BaseSpider;
from com.anjie.spider.house import House;


# Created by zaizai at 2017/9/22


class AnJuKeSpider(BaseSpider):
    def __init__(self):
        super(AnJuKeSpider, self).__init__();
        self.spiderName = 'AnJuKe'
        self.seed_url = ['https://gz.zu.anjuke.com/?from=navigation'];

    def pagerProcess(self, url, page):
        print('current url is %s'%url)
        next_link = [];
        list_result = page.xpath('//div[@class="maincontent"]//div[@class="zu-itemmod  "]')
        house_list = [];
        house = None;
        result_list = [];
        for node in list_result:
            h = House();
            # print(etree.tostring(node,encoding="utf-8",pretty_print=True,method="html").decode())
            # 抽取
            title = node.xpath('.//div[@class="zu-info"]/h3/a/text()');
            h.title = title;
            # 抽取链接
            url = node.xpath('.//div[@class="zu-info"]/h3/a/@href')
            h.url = url;
            temp = node.xpath('.//div[@class="zu-info"]/p[1]/text()')
            (house_type, sale_type, level, floor_number) = temp;
            h.house_type = house_type;
            h.sale_type = sale_type;
            h.level = level;
            h.floor_number = floor_number;
            # 抽取地址
            area_name = node.xpath('.//div[@class="zu-info"]/address/a/text()')
            h.area_name = area_name;
            area = node.xpath('.//div[@class="zu-info"]/address/text()')
            for ele in area:
                if len(ele.strip()) > 0:
                    area = ele.strip();
                    break;
            h.addr = area;
            # 抽取联系人
            user = node.xpath('.//div[@class="zu-info"]/p[2]/span/text()')
            h.user = user;
            supplement = node.xpath('.//div[@class="zu-info"]/p[2]/em/text()')
            h.supplement = supplement;

            # 获取价格
            price = node.xpath('.//div[@class="zu-side"]//strong/text()')

            h.price = price;
            unit = node.xpath('.//div[@class="zu-side"]/p/text()')
            h.unit = unit;
            result_list.append(h);

        links = page.xpath('//*[@class="multi-page"]/a/@href');
        # 利用集合过滤重复的链接
        s = set(links)
        next_link = list(s);
        print('抽取的链接:%s' % next_link)
        self.pipeline_item = result_list;
        self.addRequest_urls(next_link);
