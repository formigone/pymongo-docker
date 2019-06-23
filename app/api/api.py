from flask import Flask, jsonify, make_response
import logging
import os
import pymongo
import random

app = Flask(__name__)

logger = logging.Logger(__name__, level=os.getenv('LOGLEVEL', 'INFO'))
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-12s [%(levelname)s] %(module)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)

MONGO_HOST = os.getenv('MONGO_HOST', '0.0.0.0')
logger.info('MONGO_HOST = {}'.format(MONGO_HOST))
client = pymongo.MongoClient('mongodb://{}:27017/'.format(MONGO_HOST))
db = client.dbi_ml


def gen_response(data, code=200):
    return make_response(jsonify(data), code)


@app.errorhandler(404)
def page_not_found(error):
    return gen_response({'error': 'Route not found'}, 404)


def fetch_cars():
    cars = []
    for row in db.cars.find():
        row['_id'] = str(row['_id'])
        cars.append(row)
    return cars


@app.route('/', methods=['GET'])
def home():
    data = {
        'cars': fetch_cars(),
    }
    return gen_response(data)


if __name__ == '__main__':
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['LOGLEVEL'] = os.getenv('LOGLEVEL', 'DEBUG')
    app.run()
