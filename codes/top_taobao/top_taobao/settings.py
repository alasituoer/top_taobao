# -*- coding: utf-8 -*-

# Scrapy settings for top_taobao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'top_taobao'

SPIDER_MODULES = ['top_taobao.spiders']
NEWSPIDER_MODULE = 'top_taobao.spiders'

DOWNLOAD_DELAY = 0.25

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'top_taobao (+http://www.yourdomain.com)'
#USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22 AlexaToolbar/alxg-3.1"
