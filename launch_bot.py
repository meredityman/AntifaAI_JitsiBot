
import argparse
from distutils.log import debug
import json

from bot import socketio, create_app


PERFORMANCES_FILE = "bot/static/performances.json"
performances = json.load(open(PERFORMANCES_FILE, 'r'))['performances']


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name" , default="DEBUG")
    parser.add_argument("--bname", default="Bot")
    parser.add_argument("--aname", default="Avatar")
    parser.add_argument("--oname", default="Operator")
    parser.add_argument("--ping" , action="store_true")
    parser.add_argument("--debug" , action="store_true")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()

    performance = [p for p in performances if p['id'] == args.name]
    assert(len(performance) == 1 )
    d = vars(args)
    d['uuid'] = performance[0]['uuid']

    app = create_app(args)

    socketio.run(app, host='0.0.0.0')