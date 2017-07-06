#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
import configparser
import re
import base64
from lxml import etree
from pymongo import MongoClient
from time import sleep
import hashlib
import sys

base_path = os.path.split(os.path.realpath(__file__))[0]
conf_path = base_path + '/config.ini'


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
except BaseException:
    db = cli.Hawkeye

leakage_col = db.leakage
query_col = db.query
blacklist_col = db.blacklist
notice_col = db.notice


def create_session():
    github_username = get_conf('GitHub', 'USERNAME')
    github_password = get_conf('GitHub', 'PASSWORD')
    session = requests.session()
    login_page_resp = session.get('https://github.com/login').text
    authenticity_token = re.findall(
        'name="authenticity_token" type="hidden" value="(.*?)" />',
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


def crawl(query):
    session = create_session()
    search_url = 'https://github.com/search?o=desc&p={}&q={}&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93'
    for page in range(int(sys.argv[1]), int(sys.argv[2])):
        try:
            resp = session.get(
                search_url.format(
                    page, query['keyword']))
        except BaseException:
            sleep(30)
            resp = session.get(
                search_url.format(
                    page, query['keyword']))

        if get_conf('GitHub', 'ERROR') in resp.text:
            print('登录失败')
            exit(0)
        tree = etree.HTML(resp.text)
        nodes = tree.xpath(get_conf('Leakage', 'NODES'))
        for node in nodes:
            sleep(3)
            try:
                node_index = nodes.index(node) + 1
                in_blacklist = False
                leakage = {}
                print('datetime')
                leakage['datetime'] = node.xpath(
                    get_conf('Leakage', 'DATETIME').format(
                        node_index))[0].attrib['datetime']
                print(leakage['datetime'])
                print('link')
                leakage['link'] = 'https://github.com{}'.format(
                    node.xpath(get_conf('Leakage', 'LINK').format(node_index))[
                        0].attrib['href'])
                print(leakage['link'])
                leakage['project'] = node.xpath(
                    get_conf('Leakage', 'PROJECT').format(node_index))[0].text
                print('project')
                for blacklist in blacklist_col.find({}):
                    print(blacklist['keyword'])
                    print('\n' in blacklist['keyword'])
                    if blacklist['keyword'].lower() in leakage['link'].lower():
                        in_blacklist = True
                        break
                if in_blacklist:
                    pass
                elif leakage_col.find_one({"project": leakage['project'], "ignore": 1}):
                    pass
                elif leakage_col.find_one({"link": leakage['link'], "datetime": leakage['datetime']}):
                    pass
                else:
                    leakage['username'] = node.xpath(
                        get_conf(
                            'Leakage',
                            'USERNAME').format(node_index))[0].attrib['href'].replace(
                        '/',
                        '')
                    if len(node.xpath('span')):
                        leakage['language'] = node.xpath(
                            'span')[0].text.strip()
                    raw = 'https://raw.githubusercontent.com{}'.format(
                        node.xpath(get_conf('Leakage', 'RAW').format(node_index))[
                            0].attrib['href'].replace('/blob', ''))
                    code = requests.get(raw).text

                    leakage['code'] = base64.b64encode(
                        code.encode(encoding='utf-8')).decode()
                    leakage['_id'] = md5(leakage['code'])
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
                    leakage_col.save(leakage)
                    try:
                        if int(get_conf('Notice', 'ENABLE')):
                            send_mail(
                                '''
                                命中规则: {}\n
                                文件地址: {}\n
                                代码: \n{}
                                '''.format(
                                    leakage['tag'], leakage['link'], code))
                        else:
                            pass
                    except BaseException:
                        pass
            except Exception as e:
                print(e)
        if 'next_page disabled' in resp.text:
            break


def send_mail(content):
    receivers = []
    to_list = list(notice_col.find({}))
    for i in to_list:
        receivers.append(i['keyword'])
    mail_host = get_conf('Notice', 'MAIL_SERVER')
    mail_user = get_conf('Notice', 'FROM')
    mail_pass = get_conf('Notice', 'PASSWORD')
    sender = get_conf('Notice', 'FROM')
    message = MIMEText(content, _subtype='plain', _charset='utf-8')
    message['From'] = Header('GitHub 监控<{}>'.format(mail_user), 'utf-8')
    message['To'] = Header(','.join(receivers), 'utf-8')
    message['Subject'] = Header('[GitHub] 监控告警', 'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, 587)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, ','.join(receivers), message.as_string())
        print("邮件发送成功")
        smtp.close()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def md5(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    result = m.hexdigest()
    return result


if __name__ == '__main__':
    for query in query_col.find()[::]:
        print(query['tag'])
        crawl(query)
