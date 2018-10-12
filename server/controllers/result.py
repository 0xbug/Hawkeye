from flask import jsonify
from flask_restful import Resource, reqparse
from config.database import result_col, DESCENDING
import json


class Leakage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        parser.add_argument('language', type=str, help='')
        parser.add_argument('limit', type=int, default=10, help='')
        parser.add_argument('from', type=int, default=1, help='')
        args = parser.parse_args()
        status = json.loads(args.get('status'))
        filters = status
        if args.get('tag'):
            filters = dict({'tag': args.get('tag')}, **filters)
        if args.get('language'):
            filters = dict({'language': args.get('language')}, **filters)
        results = list(
            result_col.find(filters, {'code': 0, 'affect': 0}).sort('datetime', DESCENDING).limit(
                args.get('limit')).skip(
                args.get('limit') * (args.get('from') - 1)))
        total = result_col.count(filters)
        if total:
            msg = '共 {} 条记录'.format(total)
        else:
            msg = '暂无数据'
        data = {
            'msg': msg,
            'status': 200,
            'result': results,
            'total': total
        }
        return jsonify(data)

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='')
        parser.add_argument('project', type=str, help='')
        parser.add_argument('ignore', type=int, choices=(0, 1), help='')
        parser.add_argument('security', type=int, choices=(0, 1), help='')
        parser.add_argument('desc', type=str, default='', help='')
        args = parser.parse_args()
        desc = args.get('desc')
        result_col.update({'_id': args.get('id')}, {'$set': {'security': int(
            args.get('security')), 'ignore': int(args.get('ignore')), 'desc': desc}})
        if not args.get('security'):
            if not args.get('ignore'):
                result_col.update_many({'project': args.get('project')}, {
                    '$set': {'security': 0, 'ignore': 0, 'desc': desc}})
        if args.get('security') and args.get('ignore'):
            result_col.update_many({'project': args.get('project')}, {
                '$set': {'security': 1, 'ignore': 1, 'desc': desc}})
        data = {'status': 201, 'msg': '处理成功', 'result': []}
        return jsonify(data)


class LeakageCode(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='leakage_id')
        args = parser.parse_args()
        leakage_id = args.get('id')
        result = result_col.find_one(
            {'_id': leakage_id}, {'_id': 0, 'code': 1, 'affect': 1})
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)


class LeakageInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='leakage_id')
        args = parser.parse_args()
        leakage_id = args.get('id')
        result = result_col.find_one(
            {'_id': leakage_id}, {'_id': 0, 'code': 0})
        data = {'status': 200, 'msg': '获取信息成功', 'result': result}
        return jsonify(data)
