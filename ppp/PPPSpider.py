from kr.config import REDIS_CLIENT
from kr.config import MONGO_CLIENT
import requests
from utils.base import BaseSpider
import json
import time
from parsel import Selector
import xlwt

class PPPSpider(BaseSpider):
    website = 'ppp'
    key_name = 'info'
    project_tpl = 'http://www.cpppc.org:8082/efmisweb/ppp/projectLibrary/getProjInfoNational.do?projId=%s'
    list_tpl = 'http://www.cpppc.org:8082/efmisweb/ppp/projectLibrary/getPPPList.do?tokenid=null'

    title_x = '//div[@class="margin"]//center//font//text()'
    re_time_x = '//div[@class="margin"]//center//text()'
    details_x = '//div[@class="margin"]//table[@class="view_table"]//text()'

    def get_list(self, page_num):
        payload = {'queryPage': page_num}
        resp = requests.post(self.list_tpl, params=payload).text
        resp_json = json.loads(resp)
        return resp_json

    def get_proj(self, proj_id):
        coll = MONGO_CLIENT['ppp']['proj_text']
        pro_url = self.project_tpl % proj_id
        resp = self.p_get(pro_url).text
        proj = {}
        print(proj_id)
        proj['_id'] = proj_id
        proj['text'] = resp
        self.save_doc(coll, proj)

    def parse(self, id):
        coll = MONGO_CLIENT['ppp']['proj_text']
        resp = coll.find_one({'_id': id})['text']
        hxs = Selector(text=resp)
        title_re_time = list(self.parse_value(hxs, self.re_time_x))
        details = list(self.parse_value(hxs, self.details_x))
        # print(details)
        title = title_re_time[0]
        re_time = title_re_time[1]
        keywords = ['所在地区', '所属行业', '项目总投资', '所处阶段', '发起时间', '回报机制', '项目示范级别/批次', '项目联系人', '联系电话']
        proj_dict = {}
        proj_dict['项目名称'] = title
        proj_dict['项目发布时间'] = re_time.replace('项目发布时间：', '')
        for keyword in keywords:
            for i in range(len(details)):
                if details[i] == keyword:
                    try:
                        if details[i + 1] not in keywords:
                            proj_dict[keyword] = details[i + 1]
                        else:
                            proj_dict[keyword] = 'null'
                    except Exception as e:
                        proj_dict[keyword] = 'null'

        return proj_dict
        # print(title, re_time, area, trade, money, state, start_time, get_form, level, man, phone)

    def parse_detail(self, id):
        coll = MONGO_CLIENT['ppp']['proj_text']
        resp = coll.find_one({'_id': id})['text']
        hxs = Selector(text=resp)
        shibie_jishi_xiangmugaikuang = list(self.parse_value(hxs, self.shibie_jishi_xiangmugaikuang_x))[0]
        print(shibie_jishi_xiangmugaikuang)

    def output_example(self, id):
        coll = MONGO_CLIENT['ppp']['proj_text']
        resp = coll.find_one({'_id': id})['text']
        with open('example.html', 'w', encoding='utf8') as f_example:
            f_example.write(resp)
        print('ok')


if __name__ == '__main__':
    spider = PPPSpider()

    lines = open('id_f.txt').readlines()
    id_0 = lines[0].replace('\n', '')
    spider.parse_detail(id_0)
    spider.output_example(id_0)


    # f = xlwt.Workbook()
    # sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)
    # header = ['项目名称', '项目发布时间', '所在地区', '所属行业', '项目总投资', '所处阶段', '发起时间', '回报机制', '项目示范级别/批次', '项目联系人', '联系电话', '项目地址']
    # for i in range(len(header)):
    #     sheet1.write(0, i, header[i])
    # for i in range(1, len(lines) + 1):
    #     proj_id = lines[i -1].replace('\n', '')
    #     proj_dict = spider.parse(proj_id)
    #     for j in range(len(header) - 1):
    #         sheet1.write(i, j, proj_dict[header[j]])
    #     sheet1.write(i, len(header) - 1, spider.project_tpl % proj_id)
    #     if i % 50 == 0:
    #         print(i)
    # f.save('ppp_1.xls')
    # for line in lines:
    #     proj_id = line.replace('\n', '')
    #     proj_dict = spider.parse(proj_id)
    #     proj_info = []
    #     for key in header:
    #         proj_info.append(proj_dict[key])


