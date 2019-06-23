from flask import Flask, request, jsonify, make_response
import logging
import os
import pymongo

app = Flask(__name__)

logger = logging.Logger(__name__, level=os.getenv('LOGLEVEL', 'INFO'))
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-12s [%(levelname)s] %(module)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)

MONGO_HOST = os.getenv('MONGO_HOST', 'mongo')
logger.info('MONGO_HOST = {}'.format(MONGO_HOST))
client = pymongo.MongoClient('mongodb://{}:27017/'.format(MONGO_HOST))
db = client.dbi_ml


def gen_response(data, code=200):
    return make_response(jsonify(data), code)


@app.errorhandler(404)
def page_not_found(error):
    return gen_response({'error': 'Route not found'}, 404)


def fetch_cars(make=None, model=None, year=None):
    cars = []
    where = {}

    if make is not None:
        if isinstance(make, str):
            make = [str(val).strip() for val in make.split(',')]
        where['make'] = {'$in': make}

    if model is not None:
        if isinstance(model, str):
            model = [str(val).strip() for val in model.split(',')]
        where['model'] = {'$in': model}

    if year is not None:
        if isinstance(year, str):
            year = [int(val) for val in year.split(',')]
        where['year'] = {'$in': year}

    logger.info('Query: {}'.format(where))
    for row in db.cars.find(where):
        row['_id'] = str(row['_id'])
        cars.append(row)
    return cars


@app.route('/', methods=['GET'])
def home():
    data = {
        'cars': fetch_cars(),
    }
    return gen_response(data)


@app.route('/car/<make>', methods=['GET'])
def car_make(make):
    valid_props = ['model', 'year']
    props = {
        'make': make
    }

    for prop in valid_props:
        if prop in request.args:
            props[prop] = request.args[prop]
    data = fetch_cars(**props)
    return gen_response(data)


if __name__ == '__main__':
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['MONGO_HOST'] = '0.0.0.0'
    os.environ['LOGLEVEL'] = os.getenv('LOGLEVEL', 'DEBUG')
    app.run()
