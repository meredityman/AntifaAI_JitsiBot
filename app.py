import time
import json
import argparse
import json
from app import socketio, create_app

PERFORMANCES_FILE = "performances.json"
performances = json.load(open(PERFORMANCES_FILE, 'r'))['performances']

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name" , default="DEBUG")
    parser.add_argument("--bname", default="Bot")
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

    socketio.run(app)
