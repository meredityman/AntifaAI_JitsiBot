from pexpect import TIMEOUT
import requests
import argparse
import os
import readline
from prompts import prompt_option
from colorama import init, Fore, Back, Style
init(autoreset=True)


USE_API = True

parser = argparse.ArgumentParser(description='')
parser.add_argument('--user', type=str, required = True)
parser.add_argument('--users', type=str, nargs='+')


args = parser.parse_args()

INTERFACE_IP = "GoodOmen.local"
INTERFACE_PORT = 5001

TIMEOUT = 10



def StartInterface(interaction_type, users):
    if USE_API:
        r = requests.post(
            f'http://{INTERFACE_IP}:{INTERFACE_PORT}/engine-start/{interaction_type}', 
            json = {"users" : users},
            timeout=TIMEOUT
        )
        return r.json()
    else:
        raise

def MessageInterface(interface_id, data):
    if USE_API:
        r = requests.post(
            f'http://{INTERFACE_IP}:{INTERFACE_PORT}/engine-message/{interface_id}',
            json = data,
            timeout=TIMEOUT
        )
        return r.json()
    else:
        raise

def StopInterface(interface_id):
    if USE_API:
        r = requests.post(
                f'http://{INTERFACE_IP}:{INTERFACE_PORT}/engine-stop/{interface_id}',
                timeout=TIMEOUT
        )
        return r.json()
    else:
        raise

def printMessages(ret, debug = False):
    if debug:
        for msg in ret["messages"]:
            print(f">> {msg['channel']}:{msg['user']} -> '{msg['message']}'")
    else:
        for msg in ret["messages"]:
            print(f"{Fore.RESET}{msg['message']}\n")

def runInterface(type, args):
    ret = StartInterface(type, users=args.users)
    interface_id = ret["interface_id"]

    printMessages(ret)

    for msg in ret["messages"]:
        print(f">> {msg['channel']}:{msg['user']} -> '{msg['message']}'")


    finished = False
    while not finished:
        try:
            message = input(f"{Fore.GREEN}>> ")

            data = {
                "user"    : args.user,
                "message" : message,
                "channel" : "private"
            }

            ret = MessageInterface(interface_id, data)

            print("\n")
            printMessages(ret)
            if ret['complete']:
                break
        except KeyboardInterrupt:
            break
    
    try:
        ret = StopInterface(interface_id)
        printMessages(ret)
    except Exception as e:
        print(e)

def runGame(type, args):
    pass

TYPES = {
    "Hatespeech"     : runInterface,
    "Telegram Rating": runInterface,
    "Twitter Rating" : runInterface,
    "Incidents"      : runInterface,
    "Game"           : runGame
}

if __name__ == '__main__':

    while True:
        selected_type = None
        while not selected_type:
            os.system('clear')

            text = "\n\t".join([ f"{i+1}: {o}" for i, o in enumerate(TYPES.keys())])
            print("What interactions would you like to try?:\n\t{0}\n".format(text))


            t = input(f"Select: {Fore.GREEN}")
            selected_type, response = prompt_option(t, list(TYPES.keys()))
            if selected_type:
                print(f"{Fore.GREEN}{response}\n")
            else:
                print(f"{Fore.RED}{response}\n")
    

        TYPES[selected_type](selected_type, args)


