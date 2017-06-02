#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from crontab import CronTab
import os
import hashlib
import base64

cli = MongoClient()
db = cli.Hawkeye
leakage_col = db.leakage
query_col = db.query
blacklist_col = db.blacklist
notice_col = db.notice

app = Flask(__name__)


@app.route('/')
@app.route('/processed')
@app.route('/processing')
def index():
    return render_template('index.html')


@app.route('/statistics')
def statistics():
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
    return jsonify({'status': 200, 'result': results})


@app.route('/view/leakages/<filter_str>', methods=['GET'])
def leakages(filter_str):
    datas = []
    if filter_str == 'all':
        querys = list(query_col.find({}, {'keyword': 0}))
        for query in querys:
            results = list(leakage_col.find({'tag': query['tag'], 'security': 0}, {
                           'code': 0, 'detail': 0}).sort('datetime', 1).limit(5))
            if results:
                query['results'] = results
                datas.append(query)
    elif filter_str == 'processing':
        datas = []
        querys = list(query_col.find({}))
        for query in querys:
            results = list(leakage_col.find({'tag': query['tag'], 'security': 0, 'desc': {
                           '$exists': True}}, {'code': 0, 'detail': 0}).sort('datetime', 1))
            query['results'] = results
            datas.append(query)

    elif filter_str == 'processed':
        datas = []
        querys = list(query_col.find({}))
        for query in querys:
            results = list(leakage_col.find({'tag': query['tag'], 'security': 1}, {
                           'code': 0, 'detail': 0}).sort('datetime', 1).limit(5))
            query['results'] = results
            datas.append(query)
    else:
        datas = []
        querys = list(query_col.find({'tag': filter_str}, {'keyword': 0}))
        for query in querys:
            results = list(leakage_col.find({'tag': query['tag']}, {
                'code': 0, 'detail': 0}).sort('datetime', 1).sort('security', 1))
            query['results'] = results
            datas.append(query)
    return jsonify({'status': {'status_code': 200}, 'result': datas})


@app.route('/view/tag/<tag>')
def tag_details(tag):
    return render_template('index.html')


@app.route('/view/leakage/<leakage_id>')
def leakage_details(leakage_id):
    results = leakage_col.find_one({'_id': leakage_id})
    return render_template('detail.html', results=results)


@app.route('/view/leakage/<leakage_id>/code')
def leakage_code(leakage_id):
    results = list(leakage_col.find(
        {'_id': leakage_id}, {'_id': 0, 'code': 1}))
    return jsonify({'status': {'status_code': 200}, 'result': results})


@app.route('/deal/leakage', methods=['POST'])
def deal_leakage():
    data = request.get_json()
    desc = base64.b64encode(data['desc'].encode(encoding='utf-8')).decode()

    leakage_col.update({'_id': data['id']}, {'$set': {'security': int(
        data['security']), 'ignore': int(data['ignore']), 'desc': desc}})
    if not data['security']:
        if not data['ignore']:
            for leakage in leakage_col.find({'project': data['project']}):
                leakage_col.update({'_id': leakage['_id']}, {
                    '$set': {'security': 0, 'ignore': 0, 'desc': desc}})
    if data['security'] and data['ignore']:
        for leakage in leakage_col.find({'project': data['project']}):
            leakage_col.update({'_id': leakage['_id']}, {
                '$set': {'security': 1, 'ignore': 1, 'desc': desc}})
    return jsonify({'status': {'status_code': 200}, 'result': []})


@app.route('/setting/blacklist', methods=['GET', 'POST', 'DELETE'])
def set_blacklist():
    if request.method == 'GET':
        blacklists = list(blacklist_col.find({}, {'_id': 0}))
        return jsonify({'status': {'status_code': 200}, 'result': blacklists})
    else:
        data = request.get_json()
        keyword = data['keyword']
    if request.method == 'DELETE':
        blacklist_col.delete_many({'keyword': keyword})
    if request.method == 'POST':
        keyword = keyword.strip().replace(' ', '')
        blacklist_col.save({'_id': md5(keyword), 'keyword': keyword})

    return jsonify({'status': {'status_code': 200}, 'result': []})


@app.route('/setting/notice', methods=['GET', 'POST', 'DELETE'])
def set_notice():
    if request.method == 'GET':
        notices = list(notice_col.find({}, {'_id': 0}))
        return jsonify({'status': {'status_code': 200}, 'result': notices})
    else:
        data = request.get_json()
        keyword = data['keyword']
    if request.method == 'DELETE':
        notice_col.delete_many({'keyword': keyword})
    if request.method == 'POST':
        keyword = keyword.strip().replace(' ', '')
        notice_col.save({'_id': md5(keyword), 'keyword': keyword})

    return jsonify({'status': {'status_code': 200}, 'result': []})


@app.route('/setting/query', methods=['GET', 'POST', 'DELETE'])
def set_query():
    if request.method == 'POST':
        query = request.get_json()
        status_code = insert(query)
        return jsonify({'status': {'status_code': status_code}, 'result': []})
    elif request.method == 'DELETE':
        query = request.get_json()
        query_col.delete_many({'_id': query.get('_id')})
        leakage_col.delete_many({'tag': query.get('tag')})
        return jsonify({'status': {'status_code': 200}, 'result': []})
    else:
        querys = list(query_col.find({}))
        return jsonify({'status': {'status_code': 200}, 'result': querys})


@app.route('/setting/cron', methods=['GET', 'POST'])
def set_cron():
    if request.method == 'POST':
        data = request.get_json()
        write_cron(int(data['every']), int(data['page'] + 1))
        return jsonify({'status': {'status_code': 200}, 'result': []})
    else:
        return jsonify({'status': {'status_code': 200}, 'result': read_cron()})


@app.route('/setting', methods=['GET'])
def setting():
    return render_template('setting.html')


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
