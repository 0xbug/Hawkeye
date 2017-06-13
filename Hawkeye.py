#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from crontab import CronTab
# from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
import configparser
import json
import os
import hashlib
import base64

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

app = Flask(__name__)
api = Api(app)
# CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


class Leakage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        parser.add_argument('limit', type=int, default=10, help='')
        parser.add_argument('from', type=int, default=1, help='')
        args = parser.parse_args()
        status = json.loads(args.get('status'))
        filters = status

        if args.get('tag'):
            filters = dict({'tag': args.get('tag')}, **filters)
        results = list(
            leakage_col.find(filters, {'code': 0, 'detail': 0}).sort('datetime', 1).limit(args.get('limit')).skip(
                args.get('limit') * (args.get('from') - 1)))
        total = leakage_col.count(filters)
        if total:
            msg = '共 {} 条记录'.format(total)
        else:
            msg = '暂无数据'
        data = {
            'msg': msg,
            'result': results,
            'total': total
        }
        return jsonify(data)

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='')
        parser.add_argument('project', type=str, help='')
        parser.add_argument('ignore', type=bool, help='')
        parser.add_argument('security', type=bool, default=10, help='')
        parser.add_argument('desc', type=str, default=1, help='')
        args = parser.parse_args()
        desc = base64.b64encode(args.get('desc').encode(encoding='utf-8')).decode()

        leakage_col.update({'_id': args.get('id')}, {'$set': {'security': int(
            args.get('security')), 'ignore': int(args.get('ignore')), 'desc': desc}})
        if not args.get('security'):
            if not args.get('ignore'):
                for leakage in leakage_col.find({'project': args.get('project')}):
                    leakage_col.update({'_id': leakage['_id']}, {
                        '$set': {'security': 0, 'ignore': 0, 'desc': desc}})
        if args.get('security') and args.get('ignore'):
            for leakage in leakage_col.find({'project': args.get('project')}):
                leakage_col.update({'_id': leakage['_id']}, {
                    '$set': {'security': 1, 'ignore': 1, 'desc': desc}})
        return jsonify({'status': 200, 'msg': '处理成功', 'result': []})


api.add_resource(Leakage, '/api/leakage')


class Statistics(Resource):
    def get(self):
        pipeline = [
            {'$match': {'security': 0}},
            {'$group': {'_id': '$tag', 'value': {'$sum': 1}}},
        ]

        results = list(leakage_col.aggregate(pipeline))
        if not len(results):
            pipeline = [
                {'$group': {'_id': '$tag', 'value': {'$sum': 0}}},
            ]
            results = list(leakage_col.aggregate(pipeline))
        return jsonify({'status': 200, 'msg': '获取信息成功', 'result': results})


api.add_resource(Statistics, '/api/statistics')


@app.route('/api/leakage/<leakage_id>/code')
def leakage_code(leakage_id):
    results = list(leakage_col.find(
        {'_id': leakage_id}, {'_id': 0, 'code': 1}))
    return jsonify({'status': 200, 'msg': '获取信息成功', 'result': results})


@app.route('/api/leakage/<leakage_id>/info')
def leakage_info(leakage_id):
    results = list(leakage_col.find(
        {'_id': leakage_id}, {'_id': 0, 'code': 0}))
    return jsonify({'status': 200, 'msg': '获取信息成功', 'result': results})


class Blacklist(Resource):
    def get(self):
        blacklists = list(blacklist_col.find({}, {'_id': 0}))
        return jsonify({'status': 200, 'msg': '获取信息成功', 'result': blacklists})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help='')
        args = parser.parse_args()
        keyword = args.get('keyword')
        keyword = keyword.strip().replace(' ', '')
        blacklist_col.save({'_id': md5(keyword), 'keyword': keyword})
        blacklists = list(blacklist_col.find({}, {'_id': 0}))

        return jsonify({'status': 200, 'msg': '添加成功', 'result': blacklists})

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help='')
        args = parser.parse_args()
        blacklist_col.delete_many({'keyword': args.get('keyword')})
        blacklists = list(blacklist_col.find({}, {'_id': 0}))

        return jsonify({'status': 404, 'msg': '删除成功', 'result': blacklists})


api.add_resource(Blacklist, '/api/setting/blacklist')


class Notice(Resource):
    def get(self):
        notices = list(notice_col.find({}, {'_id': 0}))
        return jsonify({'status': 200, 'msg': '获取信息成功', 'result': notices})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help='')
        args = parser.parse_args()
        keyword = args.get('keyword')
        keyword = keyword.strip().replace(' ', '')
        notice_col.save({'_id': md5(keyword), 'keyword': keyword})
        notices = list(notice_col.find({}, {'_id': 0}))
        return jsonify({'status': 200, 'msg': '添加成功', 'result': notices})

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help='')
        args = parser.parse_args()
        notice_col.delete_many({'keyword': args.get('keyword')})
        notices = list(notice_col.find({}, {'_id': 0}))

        return jsonify({'status': 404, 'msg': '删除成功', 'result': notices})


api.add_resource(Notice, '/api/setting/notice')


class Query(Resource):
    def get(self):
        querys = list(query_col.find({}))
        return jsonify({'status': 200, 'msg': '获取信息成功', 'result': querys})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        args = parser.parse_args()
        query = args
        status_code = insert(query)
        querys = list(query_col.find({}))
        return jsonify({'status': status_code, 'msg': '添加成功', 'result': querys})

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', type=str, help='')
        parser.add_argument('tag', type=str, help='')
        args = parser.parse_args()
        query_col.delete_many({'_id': args.get('_id')})
        leakage_col.delete_many({'tag': args.get('tag')})
        querys = list(query_col.find({}))
        return jsonify({'status': 404, 'msg': '删除成功', 'result': querys})


api.add_resource(Query, '/api/setting/query')


class Cron(Resource):
    def get(self):
        return jsonify({'status': 200, 'msg': '获取信息成功', 'result': read_cron()})

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('every', type=int, help='')
        parser.add_argument('page', type=int, help='')
        args = parser.parse_args()
        write_cron(args.get('every'), int(args.get('page') + 1))
        return jsonify({'status': 200, 'msg': '修改成功', 'result': read_cron()})


api.add_resource(Cron, '/api/setting/cron')


def insert(query):
    if set(query.keys()) != {'tag', 'keyword'}:
        return 422
    elif not query_col.find_one({'tag': query.get('tag')}):
        query['_id'] = md5(''.join(query.values()))
        query_col.save(query)
        return 201
    elif query_col.find_one({'tag': query.get('tag')}):
        query_col.delete_many({'tag': query.get('tag')})
        query['_id'] = md5(''.join(query.values()))
        query_col.save(query)
        return 201
    else:
        return 200


def write_cron(time, page):
    if isinstance(time, int):
        base_path = os.path.split(os.path.realpath(__file__))[0]
        cron_command = '{0}/venv/bin/python {0}/spider.py 1 {1}'.format(
            base_path, page)
        my_user_cron = CronTab(user=True)
        if list(my_user_cron.find_command('Hawkeye')):
            for cron in my_user_cron.find_command('Hawkeye'):
                cron.delete()
        job = my_user_cron.new(command=cron_command)
        job.setall('*/{} * * * *'.format(time))
        job.set_comment("Hawkeye")
        job.enable()
        my_user_cron.write()
        return True
    else:
        return False


def read_cron():
    user_cron = CronTab(user=True)
    if list(user_cron.find_command('Hawkeye')):
        page = int(list(user_cron.find_command('Hawkeye'))
                   [0].command.split(' ')[-1]) - 1
        every = int(str(list(user_cron.find_command('Hawkeye'))
                        [0].minutes).replace('*/', ''))
        return {'every': every, 'page': page}
    else:
        return {'every': 15, 'page': 1}


def md5(message):
    m2 = hashlib.md5()
    m2.update(message.encode('utf-8'))
    results = m2.hexdigest()
    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
