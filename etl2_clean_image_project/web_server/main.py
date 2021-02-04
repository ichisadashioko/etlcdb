from bottle import route, run, template


@route('/hello/<name>')
def index(name):
    return template('hello {{name}}', name=name)


run(host='localhost', port=8888)
