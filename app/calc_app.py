from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import ast, re, random

app = Flask(__name__)
app.config['DEBUG'] = True
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('calc_app_info', 'Application info', version='1.0.3')

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
firstArg = None
secondArg = None
eMessage = 'Two numeric arguments "a" and "b" are expected.'

def evaluate_args():
    global firstArg
    global secondArg
    try:
        firstArg = ast.literal_eval(re.sub('[,]', '.', request.args.get('a')))
        secondArg = ast.literal_eval(re.sub('[,]', '.', request.args.get('b')))
        return 1
    except:
        return 0

# @app.route('/', methods=['GET'])
# def main():
#     return ""

@app.route('/add', methods=['GET'])
def add_operation():
    if evaluate_args(): return {'sum_of_numbers': firstArg + secondArg}
    return {'eMessage': eMessage}, HTTP_400_BAD_REQUEST

@app.route('/substract', methods=['GET'])
def subtract_operator():
    if evaluate_args(): return {'subtract_of_numbers': firstArg - secondArg}
    return {'eMessage': eMessage}, HTTP_400_BAD_REQUEST

@app.route('/division', methods=['GET'])
def division_operator():
    if evaluate_args(): return {'division_of_numbers': firstArg/secondArg}
    return {'eMessage': eMessage}, HTTP_400_BAD_REQUEST

@app.route('/random', methods=['GET'])
def random_operator():
    try:
        count = int(ast.literal_eval(re.sub('[,]', '.', request.args.get('count'))))
    except:
        count = 10
    return {'random_numbers':[random.randrange(-100, 100) for i in range(count)]}

@app.route('/readiness', methods=['GET'])
def readiness_probe():
    return {'readiness': 'ok'}, HTTP_200_OK

@app.route('/liveness', methods=['GET'])
def liveness_probe():
    return {'liveness': 'ok'}, HTTP_200_OK

# app.run(host="0.0.0.0",port=5000)
if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)