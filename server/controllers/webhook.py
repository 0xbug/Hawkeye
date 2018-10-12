from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from config.database import blacklist_col, result_col, query_col, notice_col, github_col, setting_col
from utils.hash import md5
from utils.date import timestamp
from github import Github
import signal
import os
import requests


class WebHook(Resource):
    def get(self):
        result = setting_col.find_one({'key': 'webhook'}, {'_id': 0})
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('webhook_url', type=str, help='webhook_url')
        parser.add_argument('enabled', type=inputs.boolean, default=False, help='enabled Notice')
        parser.add_argument('test', type=inputs.boolean, default=False, help='test')
        parser.add_argument('www_host', type=str, help='Hostname (for webhook notice link)')
        args = parser.parse_args()
        if args.get('test'):
            if not args.get('webhook_url'):
                data = {'status': 404, 'msg': '错误的webhook地址', 'result': []}
                return jsonify(data)
            test_content = {
                "msgtype": "markdown",
                "markdown": {"title": "GitHub泄露",
                             "text": '### 规则名称: [钉钉告警测试]()'
                             },
                "at": {
                    "atMobiles": [

                    ],
                    "isAtAll": False
                }
            }

            response = requests.post(
                args.get('webhook_url'),
                json=test_content)
            print(response.json())
            print(response.text())
            print(response.ok)

            data = {'status': 201, 'msg': '已发送，请查收', 'result': []}
            return jsonify(data)
        webhook_setting = args
        setting_col.update_many({'key': 'webhook'}, {'$set': dict({'key': 'webhook'}, **webhook_setting)},
                                upsert=True)
        print(webhook_setting)
        result = setting_col.find_one({'key': 'webhook'}, {'_id': 0})
        data = {'status': 201, 'msg': '设置成功', 'result': result}
        return jsonify(data)
