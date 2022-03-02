from engine import engine


import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('user', type=str)
parser.add_argument('users', type=str, nargs='+')
parser.add_argument('--id', type=str)


args = parser.parse_args()

def send_message(message):
    print(message)

def send_private_message(id, message):
    print(id, message)


def printMessages(ret):
    print("___________")
    for msg in ret["messages"]:
        print(f">> {msg['channel']}:{msg['user']} -> '{msg['message']}'")

if __name__ == '__main__':

    [print(t) for t in engine.get_types()]

    if "id" in args:
        interface_id = args.id
    else:
        ret = engine.start("Survey", users=args.users)
        print("he", ret)
        printMessages(ret)
        interface_id = ret["interface_id"]



    while True:
        try:
            message = input()

            data = {
                "user"    : args.user,
                "message" : message,
                "channel" : "private"
            }

            ret = engine.message(interface_id, data)
            printMessages(ret)
        except KeyboardInterrupt:
            break

    ret = engine.stop(interface_id)
    printMessages(ret)