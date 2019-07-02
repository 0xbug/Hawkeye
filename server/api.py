#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from controllers.result import Leakage, LeakageCode, LeakageInfo
from controllers.setting import Blacklist, Cron, Notice, Query, GithubAccount, SMTPServer, WebHookNotice
from controllers.statistic import Dashboard, Statistic
from controllers.health import Status
import re
import sys

if sys.hexversion > 0x03070000:
    re._pattern_type = re.Pattern

app = Flask(__name__)
api = Api(app)

api.add_resource(Status, '/api/health')
api.add_resource(Leakage, '/api/leakage')
api.add_resource(Cron, '/api/setting/cron')
api.add_resource(Query, '/api/setting/query')
api.add_resource(Notice, '/api/setting/notice')
api.add_resource(GithubAccount, '/api/setting/github')
api.add_resource(WebHookNotice, '/api/setting/webhook')
api.add_resource(SMTPServer, '/api/setting/mail')
api.add_resource(Dashboard, '/api/trend')
api.add_resource(Statistic, '/api/statistic')
api.add_resource(LeakageCode, '/api/leakage/code')
api.add_resource(LeakageInfo, '/api/leakage/info')
api.add_resource(Blacklist, '/api/setting/blacklist')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, use_reloader=True)
