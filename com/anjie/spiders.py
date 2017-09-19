from com.anjie.download import Download;

from lxml.html import etree;
from com.anjie.scheduler import Scheduler;
from com.anjie.module.house import House;
from com.anjie.pipeline import Pipeline;


class Spider:
    # 待抓取队列
    start_url = ['https://gz.zu.anjuke.com/?from=navigation'];

    def __init__(self):
        pass;

    def pager_back(self, current_url, html):
        next_link = [];
        root = etree.HTML(html);
        list_result = root.xpath('//div[@class="maincontent"]//div[@class="zu-itemmod  "]')
        house_list = [];
        house = None;
        print(len(list_result))
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

            #获取价格
            price = node.xpath('.//div[@class="zu-side"]//strong/text()')

            h.price = price;
            unit = node.xpath('.//div[@class="zu-side"]/p/text()')
            h.unit = unit;
            result_list.append(h);

        links = root.xpath('//*[@class="multi-page"]/a/@href');
        # 利用集合过滤重复的链接
        s = set(links)
        next_link = list(s);
        print('抽取的链接:%s' % next_link)
        return {'item': result_list, 'url': next_link}


if __name__ == '__main__':
    sp = Spider();
    sc = Scheduler(download=Download(), spider=sp, pipline=Pipeline());
    sc.start_craw();
