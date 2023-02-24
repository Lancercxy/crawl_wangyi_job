# -*- coding: utf-8 -*-
import scrapy
from wangyi.items import WangyiItem

class Wangyi01Spider(scrapy.Spider):
    name = 'wangyi01'
    allowed_domains = ['163.com']
    start_urls = ['https://hr.163.com/position/list.do']

    def parse(self, response):
        # 提取数据# 获取所有职位节点列表
        node_list = response.xpath('//*[@class="position-tb"]/tbody/tr')
        print(len(node_list))
        # 遍历节点列表
        for num, node in enumerate(node_list):
        #设置过滤条件，将目标节点获取出来
            if num % 2 == 0:
                item = WangyiItem()
                item['name'] = node.xpath('./td[1]/a/text()').extract_first()
                item['link'] = response.urljoin(node.xpath('./td[1]/a/@href').extract_first())
                item['depart'] = node.xpath('./td[2]/text()').extract_first()
                item['category'] = node.xpath('./td[3]/text()').extract_first()
                item['type'] = node.xpath('./td[4]/text()').extract_first()
                item['address'] = node.xpath('./td[5]/text()').extract_first()
                item['num'] = node.xpath('./td[6]/text()').extract_first().strip()
                item['date'] = node.xpath('./td[7]/text()').extract_first()
                # print(item)
                yield item
        # 模拟翻页
        part_url = response.xpath('/html/body/div[2]/div[2]/div[2]/div/a[last()]/@href').extract_first()
        # 判断终止条件
        if part_url != '?currentPage=10':
            next_url = response.urljoin(part_url)
            #构建请求对象，并且返回给引擎
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )