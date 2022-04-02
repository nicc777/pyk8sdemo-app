from flask import Flask
import os


app = Flask(__name__)


# @app.route("/")
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    env_str = ''
    for k, v in os.environ.items():
        env_str = '{}{}={}\n'.format(env_str, k, v)
    env_str = '{}\n\n----------\n\nOriginal Request Path: /{}'.format(env_str, path)
    return "<html><head><title>Demo App</title></head><body><h3>Demo App</h3><hr /><p>Environment:</p><pre>{}</pre></body></html>".format(env_str)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
