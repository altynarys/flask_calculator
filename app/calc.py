from flask import Flask, request, jsonify, Response
import ast, re, random

import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('request_duration_seconds', 'Histogram for the duration in seconds', buckets=(1, 2, 5, 6, 10, _INF))
graphs['c_add'] = Counter('add_request_operations_total', 'The total number of ADD requests')
graphs['h_add'] = Histogram('add_request_duration_seconds', 'Histogram of ADD requests for the duration in seconds', buckets=(1, 2, 5, 6, 10, _INF))
graphs['c_substract'] = Counter('substract_request_operations_total', 'The total number of SUBSTRACT requests')
graphs['h_substract'] = Histogram('substract_request_duration_seconds', 'Histogram of SUBSTRACT requests for the duration in seconds', buckets=(1, 2, 5, 6, 10, _INF))
graphs['c_division'] = Counter('division_request_operations_total', 'The total number of DIVISION requests')
graphs['h_division'] = Histogram('division_request_duration_seconds', 'Histogram of DIVISION requests for the duration in seconds', buckets=(1, 2, 5, 6, 10, _INF))
graphs['c_random'] = Counter('random_request_operations_total', 'The total number of RANDOM requests')
graphs['h_random'] = Histogram('random_request_duration_seconds', 'Histogram of RANDOM requests for the duration in seconds', buckets=(1, 2, 5, 6, 10, _INF))

app = Flask(__name__)
app.config['DEBUG'] = True

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

@app.route('/')
def main():
    graphs['c'].inc()
    return jsonify({'hello': 'world'}), 200

@app.route('/add')
def add_operation():
    start = time.time()
    graphs['c'].inc()
    graphs['c_add'].inc()

    time.sleep(random.randrange(20,70)/60)
    end = time.time()
    graphs['h_add'].observe(end - start)
    graphs['h'].observe(end - start)
    if evaluate_args(): return jsonify({'sum_of_numbers': firstArg + secondArg})
    return jsonify({'eMessage': eMessage}), HTTP_400_BAD_REQUEST

@app.route('/substract')
def subtract_operator():
    start = time.time()
    graphs['c'].inc()
    graphs['c_substract'].inc()

    time.sleep(random.randrange(20,70)/60)
    end = time.time()
    graphs['h_substract'].observe(end - start)
    graphs['h'].observe(end - start)

    if evaluate_args(): return jsonify({'subtract_of_numbers': firstArg - secondArg})
    return jsonify({'eMessage': eMessage}), HTTP_400_BAD_REQUEST

@app.route('/division')
def division_operator():
    start = time.time()
    graphs['c'].inc()
    graphs['c_division'].inc()

    time.sleep(random.randrange(20,70)/60)
    end = time.time()
    graphs['h_division'].observe(end - start)
    graphs['h'].observe(end - start)

    if evaluate_args(): return jsonify({'division_of_numbers': firstArg/secondArg})
    return jsonify({'eMessage': eMessage}), HTTP_400_BAD_REQUEST

@app.route('/random')
def random_operator(count=10):
    start = time.time()
    graphs['c'].inc()
    graphs['c_random'].inc()

    time.sleep(random.randrange(20,70)/60)
    end = time.time()
    graphs['h_random'].observe(end - start)
    graphs['h'].observe(end - start)

    try:
        count = int(ast.literal_eval(re.sub('[,]', '.', request.args.get('count'))))
    except:
        pass
    return jsonify({'random_numbers':[random.randrange(-100, 100) for i in range(count)]})

@app.route('/readiness')
def readiness_probe():
    graphs['c'].inc()
    return jsonify({'readiness': 'ok'}), HTTP_200_OK

@app.route('/liveness')
def liveness_probe():
    graphs['c'].inc()
    return jsonify({'liveness': 'ok'}), HTTP_200_OK

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
