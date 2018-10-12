from flask import jsonify
from flask_restful import Resource, reqparse
from config.database import blacklist_col, result_col, query_col, notice_col, github_col, setting_col

from utils.date import today_start
import psutil


class Dashboard(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tag', type=str, help='')
        args = parser.parse_args()
        tag = args.get('tag')
        if tag:
            total = {'total': result_col.count({'tag': tag}),
                     'ignore': result_col.count({'tag': tag, 'security': 1}),
                     'risk': result_col.count(
                         {'tag': tag, 'security': 0, "desc": {"$exists": True}})}
            today = {
                'total': result_col.count({'tag': tag, 'timestamp': {'$gte': today_start()}}),
                'ignore': result_col.count({'tag': tag, 'timestamp': {'$gte': today_start()}, 'security': 1}),
                'risk': result_col.count(
                    {'tag': tag, 'timestamp': {'$gte': today_start()}, 'security': 0, "desc": {"$exists": True}}),
            }
        else:
            total = {'total': result_col.count(),
                     'ignore': result_col.count({'security': 1}),
                     'risk': result_col.count(
                         {'security': 0, "desc": {"$exists": True}})}
            today = {
                'total': result_col.count({'timestamp': {'$gte': today_start()}}),
                'ignore': result_col.count({'timestamp': {'$gte': today_start()}, 'security': 1}),
                'risk': result_col.count(
                    {'timestamp': {'$gte': today_start()}, 'security': 0, "desc": {"$exists": True}}),
            }
        if setting_col.count({'key': 'task'}):
            status = psutil.pid_exists(int(setting_col.find_one({'key': 'task'}).get('pid')))
            last = setting_col.find_one({'key': 'task'}).get('last')
        else:
            status = False
            last = 0
        engine = {
            'status': status,
            'last': last,
        }
        result = {
            'all': total,
            'today': today,
            'engine': engine
        }
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)


class Statistic(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('by', type=str, default='tag', help='')
        parser.add_argument('tag', type=str, help='')
        args = parser.parse_args()
        by = args.get('by')
        tag = args.get('tag')
        if len(tag):
            filters = {'tag': tag, 'security': 0}
        else:
            filters = {'security': 0}
        pipeline = [
            {'$match': filters},
            {'$group': {'_id': '${}'.format(by), 'value': {'$sum': 1}}},
        ]

        result = list(result_col.aggregate(pipeline))
        if not len(result):
            pipeline = [
                {'$group': {'_id': '${}'.format(by), 'value': {'$sum': 0}}},
            ]
            result = list(result_col.aggregate(pipeline))
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)
