import os
import bottle

SCRIPT_PARENT, SCRIPT_FILENAME = os.path.split(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(SCRIPT_PARENT, 'static')

@bottle.route('/hello/<name>')
def hello(name='Stranger'):
    return bottle.template('hello {{name}}, how are you?', name=name)


@bottle.route('/<filepath:path>')
def serve_static(filepath):
    return bottle.static_file(filepath, root=STATIC_ROOT)


bottle.run(host='localhost', port=8888, debug=True)
