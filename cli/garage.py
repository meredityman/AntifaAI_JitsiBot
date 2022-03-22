import requests
import argparse

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

TYPES = [
    "Hatespeech",
    "Telegram Rating",
    "Twitter Rating",
    "Incidents"
]

def StartInterface(interaction_type, users):
    if USE_API:
        r = requests.post(
            f'http://{INTERFACE_IP}:{INTERFACE_PORT}/engine-start/{interaction_type}', 
            json = {"users" : users}
        )
        return r.json()
    else:
        raise

def MessageInterface(interface_id, data):
    if USE_API:
        r = requests.post(
            f'http://{INTERFACE_IP}:{INTERFACE_PORT}/engine-message/{interface_id}',
            json = data
        )
        return r.json()
    else:
        raise

def StopInterface(interface_id):
    if USE_API:
        r = requests.post(f'http://{INTERFACE_IP}:{INTERFACE_PORT}/engine-stop/{interface_id}')
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


if __name__ == '__main__':

    while True:
        selected_type = None
        while not selected_type:
            text = "\n\t".join([ f"{i+1}: {o}" for i, o in enumerate(TYPES)])
            print("What interactions would you like to try?:\n\t{0}\n".format(text))


            t = input(f"Select: {Fore.GREEN}")
            selected_type, response = prompt_option(t, TYPES)
            if selected_type:
                print(f"{Fore.GREEN}{response}\n")
            else:
                print(f"{Fore.RED}{response}\n")
    
        ret = StartInterface(selected_type, users=args.users)
        interface_id = ret["interface_id"]

        printMessages(ret)


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
            except KeyboardInterrupt:
                break

        ret = StopInterface(interface_id)
        printMessages(ret)