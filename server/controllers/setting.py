from flask import jsonify, request
from flask_restful import Resource, reqparse, inputs
from urllib.parse import urlparse
from config.database import blacklist_col, result_col, query_col, notice_col, github_col, setting_col
from utils.hash import md5
from utils.date import timestamp
from github import Github, GithubException, BadCredentialsException
import signal
import os
import requests


class System(Resource):
    def get(self):
        result = setting_col.find({'key': 'system'}, {'_id': 0})
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('argument', type=str, default=request.host, help='setting argument')
        parser.add_argument('value', type=str, default=request.host, help='setting value')
        parser.add_argument('unique', type=inputs.boolean, default=False, help='setting unique')
        args = parser.parse_args()
        value = args.get('value')
        argument = args.get('argument')

        setting_col.update_many({'key': 'system', 'argument': argument},
                                {'$set': {'key': 'system', 'argument': argument, 'value': value}}, upsert=True)

        result = list(setting_col.find({}, {'_id': 0}))
        data = {'status': 201, 'msg': '设置成功', 'result': result}
        return jsonify(data)


class Cron(Resource):
    def get(self):
        result = setting_col.find_one({'key': 'task'}, {'_id': 0})
        if result:
            data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        else:
            data = {'status': 400, 'msg': '请配置查询页数和周期', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, help='')
        parser.add_argument('minute', type=int, default=10, help='')
        args = parser.parse_args()
        page = args.get('page')
        minute = args.get('minute')
        setting_col.update_many({'key': 'task'}, {'$set': {'key': 'task', 'page': page, 'minute': minute}}, upsert=True)
        try:
            os.kill(setting_col.find_one({'key': 'task'}).get('pid'), signal.SIGHUP)
        except ProcessLookupError:
            pass
        result = list(setting_col.find({}, {'_id': 0}))
        data = {'status': 201, 'msg': '设置成功', 'result': result}
        return jsonify(data)


class GithubAccount(Resource):
    def get(self):
        result = list(github_col.find({}, {'_id': 0, 'password': 0}))
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='')
        parser.add_argument('password', type=str, help='')
        args = parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            g = Github(username, password)
            github_col.save({'_id': md5(username), 'username': username, 'password': password,
                             'mask_password': password.replace(''.join(password[2:-2]), '****'), 'addat': timestamp(),
                             'rate_limit': int(g.get_rate_limit().search.limit),
                             'rate_remaining': int(g.get_rate_limit().search.remaining)})
            result = list(github_col.find({}, {'_id': 0}))
            data = {'status': 201, 'msg': '添加成功', 'result': result}
        except BadCredentialsException:
            data = {'status': 401, 'msg': '认证失败，请检查账号是否可用', 'result': []}
        return jsonify(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='')
        args = parser.parse_args()
        github_col.delete_many({'username': args.get('username')})
        result = list(github_col.find({}, {'_id': 0}))
        data = {'status': 404, 'msg': '删除成功', 'result': result}
        return jsonify(data)


class Blacklist(Resource):
    def get(self):
        result = list(blacklist_col.find({}, {'_id': 0}))
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, help='')
        args = parser.parse_args()
        text = args.get('text')
        text = text.strip().replace(' ', '')
        blacklist_col.save({'_id': md5(text), 'text': text})
        result = list(blacklist_col.find({}, {'_id': 0}))
        data = {'status': 201, 'msg': '添加成功', 'result': result}
        return jsonify(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, help='')
        args = parser.parse_args()
        blacklist_col.delete_many({'text': args.get('text')})
        result = list(blacklist_col.find({}, {'_id': 0}))
        data = {'status': 404, 'msg': '删除成功', 'result': result}
        return jsonify(data)


class SMTPServer(Resource):
    def get(self):
        result = setting_col.find_one({'key': 'mail'}, {'_id': 0})
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=str, help='From (sender email)')
        parser.add_argument('host', type=str, help='SMTPServer Host')
        parser.add_argument('port', type=int, help='SMTPServer Port')
        parser.add_argument('tls', type=inputs.boolean, default=False, help='Force TLS')
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('password', type=str, help='Password')
        parser.add_argument('domain', type=str, help='System URL Host')
        parser.add_argument('enabled', type=inputs.boolean, default=False, help='Enabled Mail Notice')
        parser.add_argument('test', type=inputs.boolean, default=False, help='Test Mail Notice')
        args = parser.parse_args()
        __setting = args
        setting_col.update_many({'key': 'mail'}, {'$set': dict({'key': 'mail'}, **__setting)}, upsert=True)
        result = setting_col.find_one({'key': 'mail'}, {'_id': 0})
        data = {'status': 201, 'msg': '设置成功', 'result': result}
        return jsonify(data)


class WebHookNotice(Resource):
    """
    WebHook 通知
    """

    def get(self):
        result = list(setting_col.find({'webhook': {'$exists': True}}, {'_id': 0}))
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('webhook', type=str, required=True, help='WebHook URL')
        args = parser.parse_args()
        delete_result = setting_col.delete_one({'webhook': args.get('webhook')})
        if delete_result.deleted_count == 1:
            data = {'status': 200, 'msg': '删除成功', 'result': []}
        else:
            data = {'status': 404, 'msg': '删除失败', 'result': []}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('webhook', type=str, required=True, help='WebHook URL')
        parser.add_argument('domain', type=str, help='System URL Host')
        parser.add_argument('enabled', type=inputs.boolean, default=False, help='Enabled Notice')
        parser.add_argument('test', type=inputs.boolean, default=False, help='Test Notice')
        args = parser.parse_args()
        if urlparse(args.get('webhook')).netloc not in ['oapi.dingtalk.com', 'qyapi.weixin.qq.com'] or urlparse(
                args.get('webhook')).scheme != 'https':
            data = {'status': 400, 'msg': '错误的 webhook 地址', 'result': []}
            return jsonify(data)
        if args.get('test'):
            if urlparse(args.get('webhook')).netloc == 'oapi.dingtalk.com':
                test_content = {
                    "msgtype": "markdown",
                    "markdown": {"title": "GitHub泄露",
                                 "text": '### 规则名称: [WebHook告警测试]({})'.format(args.get('domain'))
                                 },
                    "at": {
                        "atMobiles": [

                        ],
                        "isAtAll": False
                    }
                }
            else:
                test_content = {
                    "msgtype": "markdown",
                    "markdown": {
                        "content": '### 规则名称: [WebHook告警测试]({})'.format(args.get('domain'))
                    }
                }

            response = requests.post(
                args.get('webhook'),
                json=test_content)
            if response.ok:
                if response.json().get('errmsg') == 'ok':
                    data = {'status': 201, 'msg': '已发送，请前往钉钉/企业微信群查看', 'result': []}
                else:
                    data = {'status': 400, 'msg': '发送失败，WebHook 响应: {}'.format(response.json().get('errmsg')),
                            'result': []}
                return jsonify(data)
            else:
                data = {'status': 400, 'msg': '发送失败，请检查服务器网络', 'result': []}
                return jsonify(data)
        del args['test']
        setting_col.update_one({'webhook': args.get('webhook')}, {'$set': args}, upsert=True)
        result = setting_col.count({'webhook': args.get('webhook')})
        if result > 0:
            data = {'status': 201, 'msg': '设置成功', 'result': result}
        else:
            data = {'status': 400, 'msg': '设置失败', 'result': result}
        return jsonify(data)


class Notice(Resource):
    def get(self):
        result = list(notice_col.find({}, {'_id': 0}))
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mail', type=str, help='')
        args = parser.parse_args()
        mail = args.get('mail')
        mail = mail.strip().replace(' ', '')
        notice_col.insert_one({'_id': md5(mail), 'mail': mail})
        result = list(notice_col.find({}, {'_id': 0}))
        data = {'status': 201, 'msg': '添加成功', 'result': result}
        return jsonify(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mail', type=str, help='')
        args = parser.parse_args()
        notice_col.delete_many({'mail': args.get('mail')})
        result = list(notice_col.find({}, {'_id': 0}))
        data = {'status': 404, 'msg': '删除成功', 'result': result}
        return jsonify(data)


class Rule(Resource):
    def get(self):
        result = list(query_col.find({}).sort('enabled', -1))
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        parser.add_argument('enabled', type=inputs.boolean, default=True, help='')
        args = parser.parse_args()
        if query_col.count({'tag': args.get('tag')}):
            query_col.update_one({'tag': args.get('tag')}, {'$set': args})
            msg = '更新成功'
        else:
            new_query = args
            new_query['_id'] = md5(''.join([str(v) for v in new_query.values()]))
            query_col.insert_one(new_query)
            msg = '添加成功'
        result = list(query_col.find({}).sort('enabled', -1))
        data = {'status': 200, 'msg': msg, 'result': result}
        return jsonify(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        args = parser.parse_args()
        query_col.delete_many({'_id': args.get('_id')})
        result_col.delete_many({'tag': args.get('tag')})
        result = list(query_col.find({}).sort('enabled', -1))
        data = {'status': 404, 'msg': '删除成功', 'result': result}
        return jsonify(data)


class Query(Resource):
    def get(self):
        result = list(query_col.find({}).sort('enabled', -1))
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        parser.add_argument('enabled', type=inputs.boolean, default=True, help='')
        args = parser.parse_args()
        if query_col.count({'tag': args.get('tag')}):
            query_col.update_one({'tag': args.get('tag')}, {'$set': args})
            msg = '更新成功'
        else:
            new_query = args
            new_query['_id'] = md5(''.join([str(v) for v in new_query.values()]))
            query_col.insert_one(new_query)
            msg = '添加成功'
        result = list(query_col.find({}).sort('enabled', -1))
        data = {'status': 200, 'msg': msg, 'result': result}
        return jsonify(data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        args = parser.parse_args()
        query_col.delete_many({'_id': args.get('_id')})
        result_col.delete_many({'tag': args.get('tag')})
        result = list(query_col.find({}).sort('enabled', -1))
        data = {'status': 404, 'msg': '删除成功', 'result': result}
        return jsonify(data)
