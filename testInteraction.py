from app.interaction import engine


ids = [ "0" ]

config = {
    # 'type': 'incidents',
    'type': 'telegram',
    'ids': ids,
} 

def send_message(message):
    print(message)

def send_private_message(id, message):
    print(id, message)


if __name__ == '__main__':

    engine.setup(config, send_message, send_private_message)
    
    while True:
        try:

            message = input()
            engine.feedEnginePrivate("0", message)

        except KeyboardInterrupt:
            break