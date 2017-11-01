from ppp.config import MONGO_CLIENT
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

    # detail xpath
    # shibie
    shibie_jishi_xmgk_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[1]/td[2]//text()'
    shibie_jishi_xmhzfw_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[2]/td[2]//text()'
    shibie_jishi_hzqx_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[3]/td[2]//text()'
    shibie_jishi_xmyzfs_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[3]/td[4]//text()'
    shibie_jishi_cgshzbfs_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[4]/td[2]//text()'
    shibie_jishi_wpp_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[5]/td[2]//text()'
    shibie_jishi_w_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[6]/td[2]/span//text()'
    shibie_jishi_zhichu_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[8]/td/table/tbody/tr[2]/td/span//text()'
    shibie_jishi_cz_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[9]/td[2]//text()'
    shibie_jishi_t_x = '//*[@id="con_ss_1"]/div/table[1]/tbody/tr[10]/td[2]/span//text()'
    shibie_shishi_wyszp_x = '//*[@id="con_ss_1"]/div/table[2]/tbody/tr[1]/td[2]/span//text()'
    shibie_shishi_czcsn_x = '//*[@id="con_ss_1"]/div/table[2]/tbody/tr[2]/td[2]/span//text()'
    shibie_shishi_sbhgk_x = '//*[@id="con_ss_1"]/div/table[2]/tbody/tr[3]/td[2]//text()'
    shibie_shishi_kxxyj_x = '//*[@id="con_ss_1"]/div/table[2]/tbody/tr[4]/td[2]/span//text()'
    shibie_shishi_sjwjj_x = '//*[@id="con_ss_1"]/div/table[2]/tbody/tr[5]/td[2]/span//text()'
    shibie_shishi_clggz_x = '//*[@id="con_ss_1"]/div/table[2]/tbody/tr[6]/td[2]/span//text()'

    def first_extra(self, list_0):
        if len(list_0) == 0:
            return 'null'
        else:
            return list_0[0]


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
        shibie_jishi_xmgk = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_xmgk_x)))
        print(shibie_jishi_xmgk)
        shibie_jishi_xmhzfw = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_xmhzfw_x)))
        print(shibie_jishi_xmhzfw)
        shibie_jishi_hzqx = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_hzqx_x)))
        print(shibie_jishi_hzqx)
        shibie_jishi_xmyzfs = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_xmyzfs_x)))
        print(shibie_jishi_xmyzfs)
        shibie_jishi_cgshzbfs = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_cgshzbfs_x)))
        print(shibie_jishi_cgshzbfs)
        shibie_jishi_wpp = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_wpp_x)))
        print(shibie_jishi_wpp)
        shibie_jishi_w = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_w_x)))
        print(shibie_jishi_w)
        shibie_jishi_zhichu = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_zhichu_x)))
        print(shibie_jishi_zhichu)
        shibie_jishi_cz = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_cz_x)))
        print(shibie_jishi_cz)
        shibie_jishi_t = self.first_extra(list(self.parse_value(hxs, self.shibie_jishi_t_x)))
        print(shibie_jishi_t)
        shibie_shishi_wyszp = self.first_extra(list(self.parse_value(hxs, self.shibie_shishi_wyszp_x)))
        print(shibie_shishi_wyszp)
        shibie_shishi_czcsn = self.first_extra(list(self.parse_value(hxs, self.shibie_shishi_czcsn_x)))
        print(shibie_shishi_czcsn)
        shibie_shishi_sbhgk = self.first_extra(list(self.parse_value(hxs, self.shibie_shishi_sbhgk_x)))
        print(shibie_shishi_sbhgk)
        shibie_shishi_kxxyj = self.first_extra(list(self.parse_value(hxs, self.shibie_shishi_kxxyj_x)))
        print(shibie_shishi_kxxyj)
        shibie_shishi_sjwjj = self.first_extra(list(self.parse_value(hxs, self.shibie_shishi_sjwjj_x)))
        print(shibie_shishi_sjwjj)
        shibie_shishi_clggz = self.first_extra(list(self.parse_value(hxs, self.shibie_shishi_clggz_x)))
        print(shibie_shishi_clggz)









    def output_example(self, id):
        coll = MONGO_CLIENT['ppp']['proj_text']
        resp = coll.find_one({'_id': id})['text']
        with open('example.html', 'w', encoding='utf8') as f_example:
            f_example.write(resp)
        print('ok')


if __name__ == '__main__':
    spider = PPPSpider()

    lines = open('ppp/id_f.txt').readlines()
    id_0 = lines[0].replace('\n', '')
    spider.parse_detail(id_0)
    # spider.output_example(id_0)
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


