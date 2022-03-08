import requests
import argparse


USE_API = True

parser = argparse.ArgumentParser(description='')
parser.add_argument('--user', type=str, required = True)
parser.add_argument('--users', type=str, nargs='+')
parser.add_argument('--id', type=str)


args = parser.parse_args()

INTERFACE_IP = "GoodOmen.local"
INTERFACE_PORT = 5001

TYPES = [
    "Hatespeech",
    "Telegram",
    "Twitter"
]

def StartInterface(interaction_type, users):
    if USE_API:
        r = requests.post(
            f'http://{INTERFACE_IP}:{INTERFACE_PORT}/engine-start/{interaction_type}', 
            json = {"users" : users}
        )
        print(r.status_code)
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

def printMessages(ret):
    print("___________")
    for msg in ret["messages"]:
        print(f">> {msg['channel']}:{msg['user']} -> '{msg['message']}'")

if __name__ == '__main__':

    
    print("Engine types:\n\t{0}\n".format("\n\t".join(TYPES)))


    if args.id is None:
        print(f"Starting session: {args.interface_type}")
        ret = StartInterface(args.interface_type, users=args.users)
        printMessages(ret)
        interface_id = ret["interface_id"]
        print(f"Created session: {interface_id }")
    else:
        interface_id = args.id
        print(f"Joining session: {interface_id}")

    while True:
        try:
            message = input()

            data = {
                "user"    : args.user,
                "message" : message,
                "channel" : "private"
            }

            ret = MessageInterface(interface_id, data)
            print(ret)
            printMessages(ret)
        except KeyboardInterrupt:
            break

    ret = StopInterface(interface_id)
    printMessages(ret)