# 现在spiders中新建一个Data文件夹
# 再以当天时间(如20161111)为名在Data中新建一个文件夹
mkdir /Users/Alas/Documents/TD_handover/压缩包/上传GitHub/top_taobao/codes/top_taobao/top_taobao/spiders/Data/`date +%Y%m%d`
# 进入该文件夹后 运行爬虫 将爬取数据存放在此
cd /Users/Alas/Documents/TD_handover/压缩包/上传GitHub/top_taobao/codes/top_taobao/top_taobao/spiders/Data/`date +%Y%m%d`
scrapy crawl top_taobao
