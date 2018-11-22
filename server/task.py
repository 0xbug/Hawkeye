import datetime
import os
import re
import random
import requests
import smtplib
import time
from ipaddress import ip_address
import tldextract
from github import Github
from huey import RedisHuey, crontab
from pymongo import errors, DESCENDING, ASCENDING
from config.database import result_col, query_col, blacklist_col, notice_col, github_col, setting_col, REDIS_HOST, \
    REDIS_PORT
from utils.date import timestamp
from utils.log import logger
from utils.notice import mail_notice

huey = RedisHuey('hawkeye', host=REDIS_HOST, port=int(REDIS_PORT))
base_path = os.path.split(os.path.realpath(__file__))[0]
extract = tldextract.TLDExtract(cache_file='{}/.tld_set'.format(base_path))

if setting_col.count({'key': 'task', 'minute': {'$exists': True}, 'page': {'$exists': True}}):
    minute = int(setting_col.find_one({'key': 'task'}).get('minute'))
    setting_col.update_one({'key': 'task'}, {'$set': {'key': 'task', 'pid': os.getpid(), 'last': timestamp()}},
                           upsert=True)

else:
    minute = 10
    setting_col.update_one({'key': 'task'},
                           {'$set': {'key': 'task', 'pid': os.getpid(), 'minute': 10, 'page': 3, 'last': timestamp()}},
                           upsert=True)


@huey.task()
def search(query, page, g, github_username):
    mail_notice_list = []
    ding_notice_list = []
    logger.info('开始抓取: tag is {} keyword is {}, page is {}'.format(
        query.get('tag'), query.get('keyword'), page + 1))
    try:
        repos = g.search_code(query=query.get('keyword'),
                              sort="indexed", order="desc")
        github_col.update_one({'username': github_username},
                              {'$set': {'rate_remaining': int(g.get_rate_limit().search.remaining)}})

    except Exception as error:
        logger.critical(error)
        logger.critical("触发限制啦")
        return
    try:
        for repo in repos.get_page(page):
            setting_col.update_one({'key': 'task'}, {'$set': {'key': 'task', 'pid': os.getpid(), 'last': timestamp()}},
                                   upsert=True)
            if not result_col.count({'_id': repo.sha}):
                try:
                    code = str(repo.content).replace('\n', '')
                except:
                    code = ''
                leakage = {
                    'link': repo.html_url,
                    'project': repo.repository.full_name,
                    'project_url': repo.repository.html_url,
                    '_id': repo.sha,
                    'language': repo.repository.language,
                    'username': repo.repository.owner.login,
                    'avatar_url': repo.repository.owner.avatar_url,
                    'filepath': repo.path,
                    'filename': repo.name,
                    'security': 0,
                    'ignore': 0,
                    'tag': query.get('tag'),
                    'code': code,
                }
                try:
                    leakage['affect'] = get_affect_assets(repo.decoded_content)
                except:
                    logger.critical(leakage.get('link'))
                    leakage['affect'] = []
                if int(repo.raw_headers.get('x-ratelimit-remaining')) == 0:
                    logger.critical('剩余使用次数: {}'.format(
                        repo.raw_headers.get('x-ratelimit-remaining')))
                    return
                last_modified = datetime.datetime.strptime(
                    repo.last_modified, '%a, %d %b %Y %H:%M:%S %Z')
                leakage['datetime'] = last_modified
                leakage['timestamp'] = last_modified.timestamp()
                in_blacklist = False
                for blacklist in blacklist_col.find({}):
                    if blacklist.get('text').lower() in leakage.get('link').lower():
                        logger.warning('{} 包含白名单中的 {}'.format(
                            leakage.get('link'), blacklist.get('text')))
                        in_blacklist = True
                if in_blacklist:
                    continue
                if result_col.count({"project": leakage.get('project'), "ignore": 1}):
                    continue
                if not result_col.count(
                        {"project": leakage.get('project'), "filepath": leakage.get("filepath"), "security": 0}):
                    mail_notice_list.append(
                        '上传时间:{} 地址: <a href={}>{}/{}</a>'.format(leakage.get('datetime'), leakage.get('link'),
                                                                  leakage.get('project'), leakage.get('filename')))
                    ding_notice_list.append(
                        '[{}/{}]({}) 上传于 {}'.format(leakage.get('project').split('.')[-1],
                                                    leakage.get('filename'), leakage.get('link'),
                                                    leakage.get('datetime')))
                try:
                    result_col.insert_one(leakage)
                    logger.info(leakage.get('project'))
                except errors.DuplicateKeyError:
                    logger.info('已存在')

                logger.info('抓取关键字：{} {}'.format(query.get('tag'), leakage.get('link')))
    except Exception as error:
        if 'Not Found' not in error.data:
            g, github_username = new_github()
            search.schedule(
                args=(query, page, g, github_username),
                delay=huey.pending_count() + huey.scheduled_count())
        logger.critical(error)
        logger.error('抓取: tag is {} keyword is {}, page is {} 失败'.format(
            query.get('tag'), query.get('keyword'), page + 1))

        return
    logger.info('抓取: tag is {} keyword is {}, page is {} 成功'.format(
        query.get('tag'), query.get('keyword'), page + 1))
    query_col.update_one({'tag': query.get('tag')},
                         {'$set': {'last': int(time.time()), 'status': 1, 'reason': '抓取第{}页成功'.format(page),
                                   'api_total': repos.totalCount,
                                   'found_total': result_col.count({'tag': query.get('tag')})}})
    if setting_col.count({'key': 'mail', 'enabled': True}) and len(mail_notice_list):
        main_content = '<h2>规则名称: {}</h2><br>{}'.format(query.get('tag'), '<br>'.join(mail_notice_list))
        send_mail(main_content)
    logger.info(len(ding_notice_list))
    if setting_col.count({'key': 'dingtalk', 'enabled': True}) and len(ding_notice_list):
        dingtalk(query.get('tag'), ding_notice_list)


@huey.task()
def dingtalk(tag, results):
    """

    :param tag:
    :param results:
    :return:
    """
    if len(results):
        hostname = setting_col.find_one({'key': 'dingtalk', 'enabled': True}).get('domain')
        webhook = setting_col.find_one({'key': 'dingtalk', 'enabled': True}).get('webhook')
        __content = {
            "msgtype": "markdown",
            "markdown": {"title": "GitHub泄露",
                         "text": '#### [规则名称: {}]({}/view/tag/{})\n\n- {}'.format(tag, hostname, tag,
                                                                                  '\n- '.join(results))
                         },
            "at": {
                "atMobiles": [

                ],
                "isAtAll": False
            }
        }

        requests.post(
            webhook,
            json=__content)


def get_domain(target):
    result = extract(target)
    if bool(len(result.suffix)) and bool(len(result.domain)):
        return '{}.{}'.format(result.domain, result.suffix)
    else:
        return False


def get_affect_assets(code):
    """

    :param code:
    :return:
    """
    code = str(code)
    affect = []
    domain_pattern = '(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}'
    ip_pattern = "(\d+\.\d+\.\d+\.\d+)"
    email_pattern = "[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
    affect_assets = {
        'domain': list(set(re.findall(domain_pattern, code))),
        'email': list(set(re.findall(email_pattern, code))),
        'ip': list(set(re.findall(ip_pattern, code))),
    }
    for assets in affect_assets.keys():
        if len(affect_assets.get(assets)) > 100:
            affect_assets[assets] = []
            continue
        for asset in affect_assets.get(assets):
            if assets == 'ip':
                if not is_ip(asset):
                    continue
            if assets == 'domain':
                if not get_domain(asset):
                    continue
            if assets == 'email':
                if not get_domain(asset.split('@')[-1]):
                    continue
            affect.append({'type': assets, 'value': asset.replace(
                "'", "").replace('"', '').replace("`", "").lower()})
    return affect


def is_ip(ip):
    """

    :param ip:
    :return:
    """
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False


@huey.task()
def send_mail(content):
    smtp_config = setting_col.find_one({'key': 'mail'})
    receivers = [data.get('mail') for data in notice_col.find({})]
    try:
        if mail_notice(smtp_config, receivers, content):
            logger.info('邮件发送成功')
        else:
            logger.critical('Error: 无法发送邮件')

    except smtplib.SMTPException as error:
        logger.critical('Error: 无法发送邮件 {}'.format(error))


@huey.periodic_task(crontab(minute='*/2'))
def update_rate_remain():
    for account in github_col.find():
        github_username = account.get('username')
        github_password = account.get('password')
        try:
            g = Github(github_username, github_password)
            github_col.update_one({'username': github_username},
                                  {'$set': {'rate_remaining': int(g.get_rate_limit().search.remaining),
                                            'rate_limit': int(g.get_rate_limit().search.limit)}})
        except Exception as error:
            logger.error(error)


def new_github():
    if github_col.count({'rate_remaining': {'$gt': 5}}):
        pass
    else:
        logger.error('请配置github账号')
        return
    github_account = random.choice(list(github_col.find({"rate_limit":{"$gt":5}}).sort('rate_remaining', DESCENDING)))
    github_username = github_account.get('username')
    github_password = github_account.get('password')
    g = Github(github_username, github_password)
    return g, github_username


@huey.periodic_task(crontab(minute='*/{}'.format(minute)))
def check():
    setting_col.update_one({'key': 'task'}, {'$set': {'key': 'task', 'pid': os.getpid()}}, upsert=True)
    query_count = query_col.count({'enabled': True})
    logger.info('需要处理的关键词总数: {}'.format(query_count))
    if query_count:
        logger.info('需要处理的关键词总数: {}'.format(query_count))
    else:
        logger.warning('请添加关键词')
        return
    if github_col.count({'rate_remaining': {'$gt': 5}}):
        pass
    else:
        logger.error('请配置github账号')
        return

    if setting_col.count({'key': 'task', 'page': {'$exists': True}}):
        setting_col.update_one({'key': 'task'}, {'$set': {'pid': os.getpid()}})
        page = int(setting_col.find_one({'key': 'task'}).get('page'))
        for p in range(0, page):
            for query in query_col.find({'enabled': True}).sort('last', ASCENDING):
                github_account = random.choice(list(github_col.find({"rate_limit":{"$gt":5}}).sort('rate_remaining', DESCENDING)))
                github_username = github_account.get('username')
                github_password = github_account.get('password')
                rate_remaining = github_account.get('rate_remaining')
                logger.info(github_username)
                logger.info(rate_remaining)
                g = Github(github_username, github_password,
                           user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36')
                search.schedule(args=(query, p, g, github_username),
                                delay=huey.pending_count() + huey.scheduled_count())
    else:
        logger.error('请在页面上配置任务参数')
