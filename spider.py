#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import configparser
import base64
import hashlib
import sys
import re
import html
import os
import smtplib
import requests
import logging
import colorlog

from email.mime.text import MIMEText
from email.header import Header

import time
from lxml import etree
from pymongo import MongoClient
from logging import handlers

base_path = os.path.split(os.path.realpath(__file__))[0]
conf_path = '{}/config.ini'.format(base_path)
log_path = '{}/logs'.format(base_path)

if os.path.isdir(log_path) is not True:
    os.mkdir(log_path, 0o755)
logfile = os.path.join(log_path, 'spider.log')

handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s [%(name)s] [%(levelname)s] %(message)s%(reset)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
handler.setFormatter(formatter)

file_handler = handlers.RotatingFileHandler(logfile, maxBytes=(1048576 * 5), backupCount=7)
file_handler.setFormatter(formatter)
logger = colorlog.getLogger('Hawkeye')
logger.addHandler(handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def hawkeye_conf():
    config = configparser.ConfigParser()
    config.read(conf_path)
    return config


def get_conf(section, option):
    config = hawkeye_conf()
    return config.get(section=section, option=option)


cli = MongoClient(host=get_conf('MongoDB', 'HOST'),
                  port=int(get_conf('MongoDB', 'PORT')))
try:
    db = cli.Hawkeye
    db.authenticate(get_conf('MongoDB', 'ACCOUNT'),
                    get_conf('MongoDB', 'PASSWORD'))
except Exception as error:
    logger.info("mongodb no auth")
    db = cli.Hawkeye

leakage_col = db.leakage
query_col = db.query
blacklist_col = db.blacklist
notice_col = db.notice

notice_list = []


def create_session():
    github_username = get_conf('GitHub', 'USERNAME')
    github_password = get_conf('GitHub', 'PASSWORD')
    session = requests.session()
    login_page_resp = session.get('https://github.com/login').text
    try:
        authenticity_token = re.findall(
            'name="authenticity_token".*?value="(.*?)" />',
            login_page_resp)[0]
        post_form = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': authenticity_token,
            'login': github_username,
            'password': github_password}
        session.post('https://github.com/session', data=post_form)
        session.get('https://github.com/settings/profile')
        return session
    except Exception as error:
        logger.critical("authenticity_token regex error:".format(error))


def crawl(query):
    session = create_session()
    search_url = 'https://github.com/search?o=desc&p={}&q={}&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93'
    for page in range(int(sys.argv[1]), int(sys.argv[2])):
        try:
            logger.info('start crawl: tag is {}, page is {}'.format(query.get('tag'), page))

            resp = session.get(
                search_url.format(
                    page, query['keyword']))
        except Exception as error:
            logger.critical(error)
            query_col.update_one({'tag': query['tag']},
                                 {'$set': {'status': -1, 'last': int(time.time()), 'reason': error}})
            resp = session.get(
                search_url.format(
                    page, query['keyword']))

        if get_conf('GitHub', 'ERROR') in resp.text:
            logger.critical('搜索失败: {}'.format(resp.text))

            query_col.update_one({'tag': query['tag']},
                                 {'$set': {'last': int(time.time()), 'status': -1, 'reason': '搜索失败'}})

            exit(0)
        tree = etree.HTML(resp.text)
        nodes = tree.xpath(get_conf('Leakage', 'NODES'))
        for node in nodes:
            try:
                node_index = nodes.index(node) + 1
                in_blacklist = False
                leakage = {}
                leakage['datetime'] = node.xpath(
                    get_conf('Leakage', 'DATETIME').format(
                        node_index))[0].attrib['datetime']
                leakage['link'] = 'https://github.com{}'.format(
                    node.xpath(get_conf('Leakage', 'LINK').format(node_index))[
                        0].attrib['href'])
                leakage['project'] = node.xpath(
                    get_conf('Leakage', 'PROJECT').format(node_index))[0].text
                leakage['_id'] = md5(leakage['link'])
                for blacklist in blacklist_col.find({}):
                    if blacklist['keyword'].lower() in leakage['link'].lower():
                        in_blacklist = True
                        break
                if in_blacklist:
                    continue
                if leakage_col.find_one({"project": leakage['project'], "ignore": 1}):
                    continue
                if leakage_col.find_one({"link": leakage['link'], "datetime": leakage['datetime']}):
                    continue
                if leakage_col.find_one({'_id': leakage['_id']}):
                    continue
                raw_link = 'https://raw.githubusercontent.com{}'.format(
                    node.xpath(get_conf('Leakage', 'RAW').format(node_index))[
                        0].attrib['href'].replace('/blob', ''))
                code_resp = requests.get(raw_link)
                code = code_resp.text.encode(
                    code_resp.encoding).decode('utf-8')
                leakage['code'] = base64.b64encode(
                    code.encode(encoding='utf-8')).decode()
                leakage['username'] = node.xpath(
                    get_conf(
                        'Leakage',
                        'USERNAME').format(node_index))[0].attrib['href'].replace(
                    '/',
                    '')
                if len(node.xpath('span')):
                    leakage['language'] = node.xpath(
                        'span')[0].text.strip()

                leakage['filename'] = node.xpath(
                    get_conf('Leakage', 'FILENAME').format(node_index))[0].attrib[
                    'title']
                leakage['tag'] = query['tag']
                leakage['detail'] = etree.tostring(
                    node, pretty_print=True, encoding='unicode').replace('{{', '<<').replace('}}', '>>').replace(
                    'href="/' + leakage['project'],
                    'target="_blank" href="https://github.com/' + leakage['project'])
                leakage['security'] = 0
                leakage['ignore'] = 0
                logger.info('{}-{}-{}'.format(query['tag'], leakage['link'], leakage['datetime']))

                leakage_col.save(leakage)

                try:
                    if leakage['project'] in notice_list:
                        pass
                    elif int(get_conf('Notice', 'ENABLE')):
                        if code:
                            code = html.escape(code)
                        else:
                            code = ''
                        email_content = '''
                                <h3>命中规则:</h3> 
                                <span>{}</span>
                                 <br>
                                <h3>文件地址:</h3>
                                <span>{}</span>
                                <br>
                                <h3>代码:</h3>
                                <pre><code style="background-color: #f6f8fa;white-space: pre;">{}</code></pre>
                                '''.format(
                            leakage['tag'], leakage['link'], code)
                        send_mail(email_content)
                        notice_list.append(leakage['project'])

                except Exception as error:
                    logger.critical(error)

            except Exception as error:
                logger.critical(error)
        query_col.update_one({'tag': query['tag']},
                             {'$set': {'last': int(time.time()), 'status': 1, 'reason': '抓取第{}页成功'.format(page)}})
        if 'next_page disabled' in resp.text:
            break
    query_col.update_one({'tag': query['tag']}, {'$set': {'last': int(time.time()), 'status': 1, 'reason': '抓取成功'}})


def send_mail(content):
    receivers = []
    to_list = list(notice_col.find({}))
    for i in to_list:
        receivers.append(i['keyword'])
    mail_host = get_conf('Notice', 'MAIL_SERVER')
    mail_port = int(get_conf('Notice', 'MAIL_PORT'))
    mail_user = get_conf('Notice', 'FROM')
    mail_pass = get_conf('Notice', 'PASSWORD')
    sender = get_conf('Notice', 'FROM')
    message = MIMEText(content, _subtype='html', _charset='utf-8')
    message['From'] = Header('GitHub 监控<{}>'.format(mail_user), 'utf-8')
    message['To'] = Header(','.join(receivers), 'utf-8')
    message['Subject'] = Header('[GitHub] 监控告警', 'utf-8')
    try:
        smtp = smtplib.SMTP(mail_host, mail_port)
        if mail_port == 587:
            smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, ','.join(receivers), message.as_string())
        smtp.close()
        logger.info('邮件发送成功')

    except smtplib.SMTPException as error:
        logger.critical('Error: 无法发送邮件 {}'.format(error))


def md5(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    result = m.hexdigest()
    return result


if __name__ == '__main__':
    for query in query_col.find({'enabled': True}).sort('status', 1):
        try:
            crawl(query)
        except Exception as error:
            logger.critical(error)
