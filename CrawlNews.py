#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
from lxml import etree
from config import pageurls
from config import get_header
from config import DEFAULT_TOTAL_CRAWL
from config import TOTAL_CHARS_SHOWS_IN_DESCRIPTION
from config import STOP_WORDS
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


def escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s

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

    news = {}
    for pageurl in pageurls:
        url = pageurl['url']

        print 'Read crawl url: ', url

        tmpurls =  url.split('/')
        rooturl = "%s//%s" % (tmpurls[0], tmpurls[2])
        isSummary = 'summary' in pageurl and pageurl['summary'] is True
        classfication = pageurl['classfication']

        page_encoding = pageurl['pageEncoding'].lower() if 'pageEncoding' in pageurl else None
        total_count = pageurl['total'] if 'total' in pageurl else DEFAULT_TOTAL_CRAWL
        pattern = pageurl['pattern']
        position = pageurl['position']
        days = pageurl['days'] if pageurl['days'] else 1
        crawl_dates = get_dates(days)


        headers = get_header()
        if pageurl.has_key('extra_headers') and type(pageurl['extra_headers']) is dict:
            headers.update(pageurl['extra_headers'])


        try:
            response = requests.get(url, headers=headers, timeout=20)
        except:
            print 'ERROR: could not visit the URL [%s]' % url
            continue

        htmlparser = etree.HTML(response.text)
        contents =  htmlparser.xpath(pattern)

        indx=0
        for content in contents:
            if total_count and total_count > 0 and indx>=total_count:
                print('Only allow Crawl top %d articles'% total_count)
                break

            te = content.xpath(position['title'])
            de = content.xpath(position['description'])
            ue = content.xpath(position['url']) if position['url'] else None
            datee = ['今天'] if position['date'] in ['today', '今天'] else content.xpath(position['date'])

            if not datee or len(datee) == 0:
                continue

            createDate = get_article_createdate(datee)
            allow_crawl = False
            for date in crawl_dates:
                allow_crawl = date in createDate
                if allow_crawl:
                    break


            # only get today write articals
            if not allow_crawl:
                continue

            if te and de:
                title = trim(te[len(te)-1])
                # the title contains stop_words
                if is_contains_stop_words(title):
                    continue

                indx+=1
                if isSummary:
                    description = etree.tostring(de[0],pretty_print=True)
                else:
                    description = trim(de[0])
                    description = description if len(description) <= TOTAL_CHARS_SHOWS_IN_DESCRIPTION else description[0:TOTAL_CHARS_SHOWS_IN_DESCRIPTION]
                    description = escape(description)

                if ue:
                    url = ue[0].strip()
                    if not (url.startswith('https') or url.startswith('http')):
                        url=rooturl + url

                title = title.encode('latin1', 'ignore').decode(page_encoding, 'ignore') if page_encoding and page_encoding != 'utf-8' else title
                description = description.encode('latin1', 'ignore').decode(page_encoding, 'ignore') if page_encoding and page_encoding != 'utf-8' else description

                if not isSummary:
                    title = replace_chars(title)
                    description = replace_chars(description)

                if not news.has_key(classfication):
                    news[classfication] = []

                news[classfication].append({
                    'isSummary': isSummary,
                    'title': title,
                    'description': description,
                    'url': url,
                    'createDate': createDate
                })

    return news

def replace_chars(v):
    return v.replace("#", '').replace('[', '\[').replace(']', '\]')

def trim(chars):
    return chars.replace('\r','').replace('\n','').replace('\r\n','').strip()

def is_contains_stop_words(str, stop_words=STOP_WORDS):
    for word in stop_words:
        if word in str:
            print 'Skipped title: %s' % str
            return True
    return False

import re
patten_d_days_ago=re.compile(r'\d{1,}\s*天前')
patten_m_d=re.compile(r'\d{1,}月\d{1,}日')
patten_y_m_d=re.compile(r'\d{1,}年\d{1,}月\d{1,}日')
patten_y_m_d_with_1 = re.compile(r'\d{1,}/\d{1,}/\d{1,}')
patten_y_m_d_with_2 = re.compile(r'\d{1,}-\d{1,}-\d{1,}')
def get_article_createdate(dates):
    now_without_time = datetime.strptime(datetime.today().strftime(DATE_FORMAT_1), DATE_FORMAT_1)
    createDate = str(trim(dates[len(dates) - 1]))
    delta_days = 0
    if createDate.isdigit():
        # it's a timestamp, e.g: 1525656310
        delta_days = (datetime.fromtimestamp(float(createDate)) - now_without_time).days

    elif '今天' in createDate or '小时前' in createDate or '分钟前' in createDate:
        delta_days=0
    elif '昨天' in createDate:
        delta_days=-1
    elif '前天' in createDate:
        delta_days = -2
    elif '天前' in createDate:
        delta_days = -int(trim(patten_d_days_ago.search(trim(createDate)).group().replace('天前', '')))

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
    tpl_article_top_summary = "<details><summary><b>{summary_title}</b></summary>{summary_content}</details>\n"
    tpl_article_content = ' ## [{title}]({url})\n > {description}\n'

    title = '%s IT News' % today
    article_title = tpl_article_title.format(category_title=title)
    article_top_summary=""
    article_content = ""


    for key in news.keys():
        if key == 'summary':
            for c in news['summary']:
                if 'isSummary' in c and c['isSummary']:
                    article_top_summary += tpl_article_top_summary.format(summary_title=c['title'],
                                                                          summary_url=c['url'],
                                                                          summary_content=c['description'])
        else:
            article_content += '# %s \n' % key
            for c in news[key]:
                article_content += tpl_article_content.format(title=c['title'], url=c['url'],
                                                              description=c['description'])

    # for c in news:
    #     if 'isSummary' in c and c['isSummary']:
    #         article_top_summary += tpl_article_top_summary.format(summary_title=c['title'], summary_url=c['url'], summary_content=c['description'])
    #         continue
    #
    #     article_content += tpl_article_content.format(title=c['title'], url=c['url'], description=c['description'])

    # article = article_title + article_top_summary+'\n' + article_content

    if article_top_summary:
        article_top_summary = article_top_summary+'\n<p>&nbsp;</p>\n'

    article = article_top_summary+ article_content
    return title, article

def create_markdown_file(title, article):
    if not (title and article):
        print 'No news info need write'
        return
    print 'start generate the markdown article.'

    filename= '%s.md' % title
    with open("./tmp/%s" % filename, 'w') as f:
        f.write(title)
        f.write(article)
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

    print 'the file name "%s" generated successfully.' % filename


def generate_files(news, create_markdown=True, create_hexo=True):
    total_news = sum([len(news[k]) for k in news])
    if total_news == 0:
        print 'No news info need write'
        return
    title, article = create_markdown_content(news)

    if create_markdown:
        create_markdown_file(title, article)

    if create_hexo:
        create_hexo_file(title, article)


if __name__ == "__main__":
    news = crawl_news()
    total_news = sum([len(news[k]) for k in news])
    print 'There are %d news will create' % total_news
    generate_files(news)
    print 'Done'