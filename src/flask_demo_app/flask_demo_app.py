from flask import Flask
import os
from flask_demo_app import Hungry


app = Flask(__name__)
monster_stomach = Hungry()


# @app.route("/")
#@app.route('/<path:path>')
@app.route('/', defaults={'path': ''})
def hello_world(path):
    env_str = ''
    for k, v in os.environ.items():
        env_str = '{}{}={}\n'.format(env_str, k, v)
    env_str = '{}\n\n----------\n\nOriginal Request Path: /{}'.format(env_str, path)
    return "<html><head><title>Demo App</title></head><body><h3>Demo App</h3><hr /><p>Environment:</p><pre>{}</pre></body></html>".format(env_str)


@app.route("/hungry")
def eat_my_memory():
    monster_stomach.eat()
    return "<html><head><title>Monster Stomach</title></head><body><h3>Stomach Contents</h3><hr /><p>{} grams of food</p></body></html>".format(len(monster_stomach.blob))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
