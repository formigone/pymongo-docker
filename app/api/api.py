from flask import Flask, jsonify, make_response
import logging
import os

app = Flask(__name__)

logger = logging.Logger(__name__, level=os.getenv('LOGLEVEL', 'INFO'))
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-12s [%(levelname)s] %(module)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


def gen_response(data, code=200):
    return make_response(jsonify(data), code)


@app.errorhandler(404)
def page_not_found(error):
    return gen_response({'error': 'Route not found'}, 404)


@app.route('/', methods=['GET'])
def home():
    data = {
        'os': dict(os.environ)
    }
    logger.info('data: {}'.format(data))
    return gen_response(data)


if __name__ == '__main__':
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['LOGLEVEL'] = os.getenv('LOGLEVEL', 'DEBUG')
    app.run()
