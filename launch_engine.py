
import argparse
from distutils.log import debug
import json
from engine import create_app
from flask_cors import CORS

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ping" , action="store_true")
    parser.add_argument("--debug" , action="store_true")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()

    app = create_app(args)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.run( host='0.0.0.0', port=5001, debug=True, use_debugger=False, use_reloader=False)
