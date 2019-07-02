from flask import jsonify
from flask_restful import Resource
from pymongo import MongoClient
import os
import requests


class Status(Resource):
    def get(self):
        try:
            github = 'api.github.com' in requests.get('https://api.github.com/', timeout=30).text
        except Exception as error:
            github = str(error)
        try:
            if os.environ.get('MONGODB_URI'):
                MONGODB_URI = os.environ.get('MONGODB_URI')
            else:
                MONGODB_URI = 'mongodb://localhost:27017'

            client = MongoClient(MONGODB_URI, connect=False, socketTimeoutMS=50)
            db = client.get_database('hawkeye')
            if os.environ.get('MONGODB_USER'):
                MONGODB_USER = os.environ.get('MONGODB_USER')
                MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
                db.authenticate(MONGODB_USER, MONGODB_PASSWORD)
            mongodb = db.last_status()
        except Exception as error:
            mongodb = str(error)
        data = {
            'github': github,
            'mongodb': mongodb,
        }
        return jsonify(data)
