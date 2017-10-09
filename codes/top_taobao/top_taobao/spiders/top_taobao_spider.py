#coding:utf-8
import scrapy
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TopTaobaoSpider(scrapy.Spider):
    name = 'top_taobao'
    allowed_domains = ['top.taobao.com', 'etao.com']
    #start_urls = ['https://top.taobao.com/?spm=a1z5i.1.2.1.hUTg2J&topId=HOME']
    start_urls = ['https://top.taobao.com']
    
    def parse(self, response):
#	print response.body
	start_str = response.body.index('mainInfo')
	end_str = response.body.index('g_srp_loadCss')
	#print start_str, end_str
#	print response.body[start_str-2:end_str-10]
	json_for_tabs = json.loads(response.body[start_str-2:end_str-10])
#	print type(json_for_tabs)
#	print json_for_tabs.keys()
#	print json_for_tabs['mods']['tab']['data']['tabs']

	# tabs = 首页 服饰 家电数码 化妆品 母婴 食品 文体 家具 车|玩具|宠物
	# 从1开始去除首页
	for info in json_for_tabs['mods']['tab']['data']['tabs'][1:]:
	    #print info['text']
	    #print info['href']
	    tab_url = 'https:' + info['href']
	    #print tab_url, '\n'
	    yield scrapy.Request(tab_url,
                      meta = {'TabName': info['text'],},
                      callback=self.parse_crawl_tabs)

    def parse_crawl_tabs(self, response): 
	start_str = response.body.index('mainInfo')
	end_str = response.body.index('g_srp_loadCss')
	json_for_panels = json.loads(response.body[start_str-2:end_str-10])
	#print response.meta['TabName'], json_for_panels.keys()
	#print response.meta['TabName']
	#print len(json_for_panels['mods']['nav']['data']['common'])
	# common = 各tabs下的品类 如"服饰"下的 "时尚女装" "靓丽女鞋" "帅气男装"...
	for info in json_for_panels['mods']['nav']['data']['common']:
	    #print info['text']
	    # sub = common 下的子品类, 如"时尚女装"下的 "连衣裙" "T恤" "毛衣"...
	    for sub_info in info['sub']:
		#print sub_info['text'], sub_info['url']
		sub_nav_url = 'https://top.taobao.com' + sub_info['url'][1:]
		yield scrapy.Request(sub_nav_url,
			meta = {
			'TabName': response.meta['TabName'],
			'NavName': info['text'],
			'SubNavName': sub_info['text'],},
                      callback=self.parse_crawl_navs)

    def parse_crawl_navs(self, response): 
	start_str = response.body.index('mainInfo')
	end_str = response.body.index('g_srp_loadCss')
	json_for_panels = json.loads(response.body[start_str-2:end_str-10])
	#print response.meta['TabName'],
	#print response.meta['NavName'],
	#print response.meta['SubNavName']
	#print json_for_panels['mods'].keys()#['bswitch']['data']['switchs']

	# switch = 销售上升榜 销售热门榜 搜索上升榜 搜索热门榜 品牌上升榜 品牌热门榜
	for types in json_for_panels['mods']['bswitch']['data']['switchs']:
	    #print types['name'],
	    #print types['url']
#	print '\n'
	    #navs_types_url = 'https://top.taobao.com' + types['url'][1:]
	    #print types['name'],
	    #print navs_types_url
#	print '\n'
	    for i in range(5):
		navs_types_url = 'https://top.taobao.com' + types['url'][1:] + '&s=' + str(i*20)
		yield scrapy.Request(navs_types_url,
			meta = {'TabName': response.meta['TabName'],
				'NavName': response.meta['NavName'],
				'SubNavName': response.meta['SubNavName'],
				'SubNavTypesName': types['name'],},
			callback=self.parse_crawl_types)

    def parse_crawl_types(self, response): 
	start_str = response.body.index('mainInfo')
	end_str = response.body.index('g_srp_loadCss')
	json_for_panels = json.loads(response.body[start_str-2:end_str-10])
#	print response.meta['TabName'],
#	print response.meta['NavName'],
#	print response.meta['SubNavName'],
#	print response.meta['SubNavTypesName'],
#	print response.url	

	#if 'li' in 'limingzhi':
	#print json_for_panels['mods'].keys()
	#print json_for_panels['mods']['wbang'].keys()
	#print json_for_panels['mods']['wbang']['data'].keys()
	#print len(json_for_panels['mods']['wbang']['data']['list'])
#	print json_for_panels['mods']['wbang']['data']['list'][0]
	for record in json_for_panels['mods']['wbang']['data']['list']:
#	    print record['col1']['text']
	    #print record['col1']['text'],
	    #print record['col2']['text'],
	    #print record['col3']#['text'],
	    #print record['col4']['num'],
	    #print record['col4']['percent'],
	    #print record['col5']['text'],
	    #print record['col5']['upOrDown']
	#print '\n'
	    if len(record['col3']) == 0:
		# 品类 子品类 排行榜类型
		# 1排名, 2关键词, 3参考价(占位,有意缺失), 4.1关注指数, 4.2关注比例显示条长度, 
		# 5.1升降位次, 5.2位次是否升降, 6.1升降幅度, 6.2幅度是否升降
		# 1升0降2持平
		strings=response.meta['NavName'] + ',' + response.meta['SubNavName'] + ',' + \
			response.meta['SubNavTypesName'] + ',' + \
			str(record['col1']['text']) + ',' + \
			str(record['col2']['text']).replace(',', ' ').replace('，', ' ') + ','*2 + \
			str(record['col4']['num']) + ',' + str(record['col4']['percent']) + ',' + \
			str(record['col5']['text']) + ',' + str(record['col5']['upOrDown']) + ',' + \
			str(record['col6']['text']) + ',' + str(record['col6']['upOrDown']) + '\n'
			# 此时的 record['col3'] = [], 连写两个逗号等于填充空值
	    else:
		# 品类 子品类 排行榜类型
		# 1排名, 2关键词, 3参考价, 4.1成交指数, 4.2成交比例显示条长度, 
		# 5.1升降位次(or幅度), 5.2位次(幅度)是否升降, 6.1升降幅度(占位,故意缺失), 6.2幅度是否升降(占位,故意缺失)
		# 1升0降2持平
		strings=response.meta['NavName'] + ',' + response.meta['SubNavName'] + ',' + \
			response.meta['SubNavTypesName'] + ',' + \
			str(record['col1']['text']) + ',' + \
			str(record['col2']['text']).replace(',', ' ').replace('，', ' ').replace('=', '等').replace('"', ' ').replace('“', ' ') + ',' + \
			str(record['col3']['text']) + ',' + \
			str(record['col4']['num']) + ',' + str(record['col4']['percent']) + ',' + \
			str(record['col5']['text']) + ',' + str(record['col5']['upOrDown']) + ','*2 + '\n'
			# 最后多写入两个逗号, 是为了保持CSV文件格式一致
			# 类似于上一种情况, record['col3']为空的时仍然做了保留 
	    if response.meta['TabName'] == '服饰':
		with open('服饰.csv', 'ab') as f:
		    f.write(strings)
	    elif response.meta['TabName'] == '数码家电':
		with open('数码家电.csv', 'ab') as f:
		    f.write(strings)
	    elif response.meta['TabName'] == '化妆品':
		with open('化妆品.csv', 'ab') as f:
		    f.write(strings)
	    elif response.meta['TabName'] == '母婴':
		with open('母婴.csv', 'ab') as f:
		    f.write(strings)
	    elif response.meta['TabName'] == '食品':
		with open('食品.csv', 'ab') as f:
		    f.write(strings)
	    elif response.meta['TabName'] == '文体':
		with open('文体.csv', 'ab') as f:
		    f.write(strings)
	    elif response.meta['TabName'] == '家居':
		with open('家居.csv', 'ab') as f:
		    f.write(strings)
	    elif response.meta['TabName'] == '车|玩具|宠物':
		with open('车|玩具|宠物.csv', 'ab') as f:
		    f.write(strings)
	    else:
		continue
	    
