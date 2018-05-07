# coding:utf-8
import random

"""
定义规则 pageurls:url列表
         type：解析方式,取值 regular(正则表达式),xpath(xpath解析),module(自定义第三方模块解析)
         days: 抓取几天的内容 (1 表示只抓取今天的文章, 2: 表示今天和昨天, ...)
         total: 共抓却多少条
         patten：可以是正则表达式,可以是xpath语句不过要和上面的相对应
"""

STOP_WORDS=['公告', '有奖辩论']

pageurls = [
    {
        'url': 'http://www.woshipm.com/news',
        'summary': True,
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[contains(@class,'u-width800')]/div",
        'position': {'title': './article[1]/h2/text()', 'description': './article[1]/div[contains(@class,"news-list-content")]', 'url':'', 'date': './time[1]/span/text()'}
    },
    {
        'url': 'http://www.woshipm.com/news',
        'summary': True,
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[contains(@class,'u-width800')]/div",
        'position': {'title': './article[2]/h2/text()', 'description': './article[2]/div[contains(@class,"news-list-content")]', 'url':'', 'date': './time[1]/span/text()'}
    },
    {
        'url': 'http://www.51cto.com/',
        'type': 'xpath',
        'days': 1,
        'pageEncoding': 'gb2312',
        'pattern': ".//div[contains(@class, 'home-right')]/div[1]/div[contains(@class,'zd-list')]/ul/li",
        'position': {'title': './a[2]/span/text()', 'description': './a[2]/span/text()', 'url':'./a[2]/@href', 'date': '今天'}
    },
    {
        'url': 'http://www.51cto.com/',
        'type': 'xpath',
        'days': 1,
        'pageEncoding': 'gb2312',
        'total': 10,
        'pattern': ".//div[contains(@class, 'home-left-list')][1]/ul/li//div[contains(@class,'rinfo')]",
        'position': {'title': './a/text()', 'description': './p/text()', 'url':'./a/@href', 'date': './div[contains(@class, "time")]/i/text()'}
    },
    {
        'url': 'https://blog.csdn.net',
        'type': 'xpath',
        'days': 1,
        'total': 15,
        'pattern': ".//ul[contains(@class, 'feedlist_mod')]/li",
        'position': {'title': './div/div[@class="title"]/h2/a/text()', 'description': './div/div[@class="title"]/h2/a/text()', 'url':'./div/div[@class="title"]/h2/a/@href', 'date': './@shown-time'}
    },
    {
        'url': 'https://blog.csdn.net/csdnnews',
        'type': 'xpath',
        'days': 2,
        'pattern': ".//div[@class='article-list']/div",
        'position': {'title': './h4/a/text()', 'description': 'p/a/text()', 'url':'./h4/a/@href', 'date': './div/p[1]/span/text()'}
    },
    {
        'url': 'https://blog.csdn.net/yunfupei0434',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@class='article-list']/div",
        'position': {'title': './h4/a/text()', 'description': './p/a/text()', 'url':'./h4/a/@href', 'date': './div/p[1]/span/text()'}

    },
    {
        'url': 'https://www.jianshu.com/u/a2c6cc53b173',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@id='list-container']/ul/li",
        'position': {'title': './div/a/text()', 'description': './div/p/text()', 'url': './div/a/@href', 'date': './div/div[@class="author"]/div/span[@class="time"]/@data-shared-at'}

    },
    {
        'url': 'https://www.jianshu.com/c/f546444928a7',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@id='list-container']/ul/li",
        'position': {'title': './div/a/text()', 'description': './div/p/text()', 'url': './div/a/@href', 'date': './div/div[@class="author"]/div/span[@class="time"]/@data-shared-at'}

    },
    {
        'url': 'https://www.jianshu.com/c/7847442e0728',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@id='list-container']/ul/li",
        'position': {'title': './div/a/text()', 'description': './div/p/text()', 'url': './div/a/@href', 'date': './div/div[@class="author"]/div/span[@class="time"]/@data-shared-at'}
    },
    {
        'url': 'https://www.jianshu.com/u/4327d37e6502',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@id='list-container']/ul/li",
        'position': {'title': './div/a/text()', 'description': './div/p/text()', 'url': './div/a/@href', 'date': './div/div[@class="author"]/div/span[@class="time"]/@data-shared-at'}

    },
    {
        'url': 'http://www.lanjingtmt.com/news',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@class='in-main-l']/dl",
        'position': {'title': './dd/h2/a/text()', 'description': './dd/p[2]/text()', 'url': './dd/h2/a/@href', 'date': './dd/p[@class="msg"]/text()'}
    },
    {
        'url': 'http://www.woshipm.com/',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[contains(@class,'home-post-list')]/div",
        'position': {'title': './div[@class="content"]/h2/a/text()', 'description': './div[@class="content"]/p/text()', 'url': './div[@class="content"]/h2/a/@href', 'date': './div[@class="content"]/div[@class="stream-list-meta"]/time/text()'}
    },
    {
        'url': 'http://www.chanpin100.com/',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@class='article-container']/div[@class='item']/div/div[@class='media-body']",
        'position': {'title': './h4/a/text()', 'description': './p[@class="article-summary"]/text()', 'url': './h4/a/@href', 'date': './ul[@class="article-info"]/li[@class="date"]/text()'}
    },
    {
        'url': 'http://www.pmtoo.com/',
        'type': 'xpath',
        'days': 1,
        'pattern': ".//div[@class='news-list']/article/div[@class='news-con']",
        'position': {'title': './h2/a/text()', 'description': './div[@class="des"]/text()', 'url': './h2/a/@href', 'date': './div[@class="author"]/div[@class="avatar-des"]/div/span[@class="time"]/text()'}
    }

    # ,
    # {
    #     'url': 'https://www.pmcaff.com/',
    #     'type': 'xpath',
    #     'days': 1,
    #     'pattern': ".//div[contains(@class,'feed')]/ul[2]/li",
    #     'position': {'title': './table/tbody/tr/td[contains(@class, "item-title")]/a/text()', 'description': './table/tbody/tr/td[contains(@class, "item-title")]/a/text()', 'url': './table/tbody/tr/td[contains(@class, "item-title")]/a/@href', 'date': './table/tbody/tr/td[contains(@class, "item-title")]/div/a[2]/@title'}
    # },
    # ,
    # {
    #     'url': '',
    #     'type': 'xpath',
    #     'pattern': "",
    #     'position': {'title': '', 'description': '', 'url': '', 'date': ''}
    #
    # }

]


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

def get_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }