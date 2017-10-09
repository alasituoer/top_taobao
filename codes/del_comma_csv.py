#coding:utf-8
import pandas as pd
import os

# 初期的淘宝热卖数据的爬取没有考虑到记录中标题一栏会含有逗号(',', '，')
# 所以此脚本就是将标题部分修改后重新生成revised_版本的文件(每天6个, 放于同一文件夹)
# 但是现在在爬取的同时就已经做了去逗号的处理
# 在201704期, 发现标题部分在开头还会有'='字符, 导致写入Excel时打开会报错并修复
# 虽然在2017年5月12日已经于服务器修改了爬虫, 让其将'='修改为'等'
# 但是截止到5月12日的数据依然存在标题中特别是开头存在'='的情况


# 得到指定路径下的文件(夹)名列表
# 每一天(以日期作为文件夹名)的路径
path1 = '/Users/Alas/Documents/TD_handover/top_taobao/data_source/2017-08/2017-08/'
date_dir_list = os.listdir(path1)
date_dir_list = [item for item in date_dir_list if '.DS_Store' not in item]
#print date_dir_list


# 将列表中的隐藏文件'.DS_Store'删除
# 为了通用删除不必要的项, 没有直接删除列表第一项而是循环查找
#print dir_list
for i,d in enumerate(date_dir_list):
    if '.DS_Store' in d:
	del date_dir_list[i]
#print date_dir_list

# 控制是在哪一天的文件夹下
for date in date_dir_list:
#for date in date_dir_list:
    path2 = path1 + '/' + date
    category_list = os.listdir(path2)

    # 删除日期文件夹下淘宝排行下文件列表中的系统文件
    for i,d in enumerate(category_list):
	if '.DS_Store' in d:
	    del category_list[i]

    # 输出每一天文件夹中的品类文件
    #print category_list
    #print date, '\t', 
#    for c in category_list:
#	print c,
#    print '\r'

    # 输出每一天文件夹中的品类文件路径
#    print date
#    for c in category_list:
#	print path2 + '/' + c
#    print '\n'

    # 在某个日期文件夹中循环打开品类文件:
    for c in category_list:
	files = open(path2 + '/revised_' + c, 'ab')
	with open(path2 + '/' + c, 'rb') as f:
#	    print date, c
	    # 打开文件
	    # 循环按行提取文件内容
	    for old_strings in f:
		# 初始化新字符串为旧字符串
		new_strings = old_strings
		# 统计该行(字符串)中逗号数量是否大于11, 如果是 那么说明标题中存在额外逗号

		#if old_strings.count(',') > 11:
		# 三字节存储一个中文字符
#		print old_strings,
#		print type(old_strings), len(old_strings)
		# 截取标题部分
		# 位于子串从前数第4个逗号和从后数第7个逗号之间
		index_list = []
		index = 1
		while True:
		    index = old_strings.find(',', index+1)
		    if index == -1:
			break
		    index_list.append(index)
		# 所有逗号的下标列表
#		print index_list
		# 将该行分为 不修改的前半部分 需要修改的标题部分 不需修改的后半部分
#		print old_strings[:index_list[3]+1]
		new_title = old_strings[index_list[3]+1:index_list[-7]]
#		print old_strings[index_list[-7]:]

		# 构建新字符串, 将需修改的部分用空格替换掉 ',' 和 '，'
		new_strings = old_strings[:index_list[3]+1] + \
		        new_title.replace('=', '(等号)').replace(',', 
                                ' ').replace('，', ' ').replace('"', '').replace('“', '') +\
		    	old_strings[index_list[-7]:]
#		print new_strings
#		print '\n'
		
		# 将新字符串写入同一文件夹下的另一个文件 命名方式是在原文件名的前边加上'Revised'
	        files.write(new_strings)
        files.close()
#print '\n'    



