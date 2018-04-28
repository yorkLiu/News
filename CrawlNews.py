#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
from lxml import etree
from config import pageurls
from config import get_header
from datetime import datetime
from datetime import timedelta

import sys
reload(sys)
sys.setdefaultencoding("utf8")

DATE_FORMAT_1='%Y-%m-%d'
DATE_FORMAT_2='%m.%d.%Y'
DATE_FORMAT_3='%Y/%m/%d'

TIME_FORMAT='%H:%M:%S'

# DATE_FORMATTER = {
#     'CSDN': DATE_FORMAT_1,
#     'jianshu': DATE_FORMAT_1
# }

today = datetime.now().strftime(DATE_FORMAT_1)
today_date_time =  datetime.now().strftime('%s %s' % (DATE_FORMAT_1, TIME_FORMAT))

def get_dates(days=1):
    dates = set([])
    dates.add(today)
    for d in range(1, days):
        dates.add((datetime.today() + timedelta(days=-d)).strftime(DATE_FORMAT_1))

    return dates

def crawl_news():
    """
    craw the news
    :return: news list
    """
    news = []
    for pageurl in pageurls:
        url = pageurl['url']
        tmpurls =  url.split('/')
        rooturl = "%s//%s" % (tmpurls[0], tmpurls[2])
        pattern = pageurl['pattern']
        position = pageurl['position']
        days = pageurl['days'] if pageurl['days'] else 1
        crawl_dates = get_dates(days)
        response = requests.get(url, headers=get_header())
        htmlparser = etree.HTML(response.text)
        contents =  htmlparser.xpath(pattern)

        ## format date
        # cdate = today.strftime(DATE_FORMAT_1)
        # for key in DATE_FORMATTER.keys():
        #     if key.lower() in url.lower():
        #         cdate = today.strftime(DATE_FORMATTER[key])
        #         break

        for content in contents:
            te = content.xpath(position['title'])
            de = content.xpath(position['description'])
            ue = content.xpath(position['url'])
            datee = content.xpath(position['date'])

            if not datee or len(datee) == 0:
                break

            createDate = get_article_createdate(datee)
            allow_crawl = False
            for date in crawl_dates:
                allow_crawl = date in createDate
                if allow_crawl:
                    break


            # only get today write articals
            if not allow_crawl:
                break

            if te and de and ue:
                title = trim(te[len(te)-1])
                description = trim(de[0])
                url = ue[0].strip()
                if not (url.startswith('https') or url.startswith('http')):
                    url=rooturl + url

            news.append({
                'title': title,
                'description': description,
                'url': url,
                'createDate': createDate
            })

    return news


def trim(chars):
    return chars.replace('\r','').replace('\n','').replace('\r\n','').strip()

import re
patten_m_d=re.compile(r'\d{1,}月\d{1,}日')
patten_y_m_d=re.compile(r'\d{1,}年\d{1,}月\d{1,}日')
patten_y_m_d_with_1 = re.compile(r'\d{1,}/\d{1,}/\d{1,}')
patten_y_m_d_with_2 = re.compile(r'\d{1,}-\d{1,}-\d{1,}')
def get_article_createdate(dates):
    now_without_time = datetime.strptime(datetime.today().strftime(DATE_FORMAT_1), DATE_FORMAT_1)
    createDate = str(trim(dates[len(dates) - 1]))
    delta_days = 0
    if '今天' in createDate or '小时前' in createDate or '分钟前' in createDate:
        delta_days=0
    elif '昨天' in createDate:
        delta_days=-1
    elif '天前' in createDate:
        delta_days = -(int(trim(createDate.replace('天前', ''))))

    elif patten_m_d.search(createDate):
        m_d = patten_m_d.search(createDate).group().replace("月", "-").replace("日", "")
        d = datetime.strptime('%s-%s' % (datetime.today().year, m_d), DATE_FORMAT_1)
        delta_days = (d - now_without_time).days

    elif patten_y_m_d.search(createDate):
        cd = patten_m_d.search(createDate).group().replace("年", "-").replace("月", "-").replace("日", "")
        d = datetime.strptime(cd, DATE_FORMAT_1)
        delta_days = (d - now_without_time).days

    elif patten_y_m_d_with_1.search(createDate):
        d = datetime.strptime(patten_y_m_d_with_1.search(createDate).group(), DATE_FORMAT_3)
        delta_days = (d - now_without_time).days

    elif patten_y_m_d_with_2.search(createDate):
        d = datetime.strptime(patten_y_m_d_with_2.search(createDate).group(), DATE_FORMAT_1)
        delta_days = (d - now_without_time).days

    return (now_without_time + timedelta(days=delta_days)).strftime(DATE_FORMAT_1)


def create_markdown_content(news):
    if len(news) == 0:
        print 'No news info need write'
        return

    tpl_article_title = "# {category_title}\n"
    tpl_article_content = ' ## [{title}]({url})\n > {description}\n'

    title = '%s IT News' % today
    article_title = tpl_article_title.format(category_title=title)
    article_content = ""
    for c in news:
        article_content += tpl_article_content.format(title=c['title'], url=c['url'], description=c['description'])

    article = article_title + article_content
    return title, article

def create_markdown_file(title, article):
    if not (title and article):
        print 'No news info need write'
        return
    print 'start generate the markdown article.'

    filename= '%s.md' % title
    with open("./tmp/%s" % filename, 'w') as f:
        f.write(article)
        f.flush()
    print 'the file name "%s" generated successfully.' % filename


def create_hexo_file(title, article):
    if not (title and article):
        print 'No news info need write'
        return
    print 'start generate the hexo article.'

    hexo_tpl = """---
title: {title}
copyright: true
date: {datetime}
tags: IT NEWS
categories: IT NEWS
---
{content}
    """

    hexo_article = hexo_tpl.format(title=title, datetime=today_date_time, content=article)
    filename = 'hexo_%s.md' % title
    with open("./tmp/%s" % filename, 'w') as f:
        f.write(hexo_article)
        f.flush()

    print 'the file name "%s" generated successfully.' % filename


def generate_files(news, create_markdown=True, create_hexo=True):
    if len(news) == 0:
        print 'No news info need write'
        return
    title, article = create_markdown_content(news)

    if create_markdown:
        create_markdown_file(title, article)

    if create_hexo:
        create_hexo_file(title, article)


if __name__ == "__main__":
    news = crawl_news()
    # news = [
    #     {'url': 'https://www.jianshu.com/p/7c5b27f4c45f', 'createDate': '2018-04-27T16:14:21+08:00',
    #      'description': u'\u84dd\u7259\u6280\u672f\u81ea1994\u5e74\u63d0\u51fa\u81f3\u4eca\uff0c\u7ecf\u4e45\u4e0d\u8870\uff0c\u4e0d\u65ad\u66f4\u65b0\u8fed\u4ee3\uff0c\u672c\u6587\u5c06\u5217\u4e3e\u51e0\u6b3e\u5982\u4eca\u4e3b\u6d41\u7684\u84dd\u7259\u82af\u7247\u6765\u4e3a\u4f60\u89e3\u8bf4\u3002                                      ...',
    #      'title': u'\u4e00\u6587\u5bf9\u6bd4\u56fd\u5185\u5916\u84dd\u7259\u82af\u7247'},
    #     {'url': 'https://www.jianshu.com/p/aaaee75f6fa4', 'createDate': '2018-04-27T15:38:38+08:00',
    #      'description': u'\u524d\u51e0\u5929\uff0c\u7f51\u4e0a\u8fc5\u901f\u8e7f\u7ea2\u4e00\u4e2a\u8bcd\u201c \u7761\u540e\u6536\u5165\u201d\uff0c\u542b\u4e49\u4e5f\u8ddf\u5b57\u9762\u610f\u601d\u4e00\u6837\u7b80\u5355\uff1a\u7761\u7740\u4ee5\u540e\uff0c\u8fd8\u80fd\u83b7\u5f97\u7684\u6536\u5165\uff01 \u73b0\u5728\u7684\u5de5\u4f5c\u65e9\u5df2\u4e0d\u50cf\u4ece\u524d\uff0c\u6bcf\u65e5\u671d\u4e5d\u665a\u4e94\u7684\u5728\u4e00\u4e2a\u5c97\u4f4d\u4e0a\u594b\u6597\uff0c\u800c\u662f\u65f6\u95f4\u8d8a\u6765\u8d8a\u81ea\u7531\uff0c\u5de5...',
    #      'title': u'\u201c\u7761\u540e\u6536\u5165\u201d\u7684\u76c8\u5229\u5185\u5e55\uff01\u6211\u540e\u6094\u6ca1\u65e9\u70b9\u77e5\u9053\uff01'},
    #     {'url': 'https://www.jianshu.com/p/89b9618b515a', 'createDate': '2018-04-27T15:30:29+08:00',
    #      'description': u'\u6b22\u8fce\u6765\u5230\u61d2\u533a\u5757\uff0c\u4eba\u4eba\u90fd\u80fd\u770b\u61c2\u7684\u533a\u5757\u94fe\u6280\u672f\u89e3\u8bfb\uff0c\u6df1\u5165\u6d45\u51fa\u7684\u89e3\u5256\u6574\u4e2a\u533a\u5757\u94fe\u7cfb\u7edf\u3002\u672c\u6587\u7531\u61d2\u533a\u5757\u6574\u7406\u64b0\u5199\uff0c\u4e0d\u7ecf\u8fc7\u5141\u8bb8\uff0c\u5207\u52ff\u8f6c\u8f7d\u3002\u672c\u7cfb\u5217\u6709\u5341\u4e8c\u7bc7\u6587\u7ae0\uff0c\u8fd9\u5341\u4e8c\u7bc7\u6587\u7ae0\u4ecb\u7ecd\u4e86\u533a\u5757\u94fe\u6280\u672f\u7684\u7b80\u53f2...',
    #      'title': u'\u533a\u5757\u94fe\u7b80\u53f2\uff08\u5341\u4e00\uff09\uff1a\u4e3a\u4ec0\u4e48\u8bf4\u8de8\u94fe\u662f\u533a\u5757\u94fe\u6280\u672f\u672a\u6765\u53d1\u5c55\u7684\u8d8b\u52bf'},
    #     {'url': 'https://www.jianshu.com/p/2a27a788e3ea', 'createDate': '2018-04-27T15:23:31+08:00',
    #      'description': u'editplus Windows\u811a\u672c\u7f16\u7a0b\u914d\u7f6e \u524d\u63d0\u8981\u6c42 \u914d\u7f6eeditplus \u6253\u5f00editplus\u7528\u6237\u5de5\u5177\u914d\u7f6e, Tools => Configure User Tools,...',
    #      'title': u'editplus Windows\u811a\u672c\u7f16\u7a0b\u914d\u7f6e'},
    #     {'url': 'https://www.jianshu.com/p/131bc5f37c68', 'createDate': '2018-04-27T09:40:07+08:00',
    #      'description': u'4\u670826\u65e5\u52304\u670828\u65e5\uff0c\u5168\u74032018 \u5168\u7403\u79fb\u52a8\u4e92\u8054\u7f51\u5927\u4f1a\uff08GMIC\uff09\u5728\u5317\u4eac\u4e3e\u884c\u3002\u5728\u4eca\u5929\u4e3e\u884c\u7684\u201c\u533a\u5757\u94fe\u51fa\u6d77\u65b0\u673a\u4f1a\u201d\u5706\u684c\u8bba\u575b\u73af\u8282\u4e2d\uff0c\u767d\u9cb8\u51fa\u6d77CEO\u9b4f\u65b9\u4e39\u3001Contento CEO...',
    #      'title': u'\u533a\u5757\u94fe\u51fa\u6d77\u65b0\u673a\u4f1a\uff1a\u4e24\u4e09\u5e74\u5185\u5fc5\u987b\u627e\u5230\u4ef7\u503c\u8bc9\u6c42\u70b9'}
    # ]

    print 'There are %d news will create' % len(news)
    generate_files(news)
    print 'Done'