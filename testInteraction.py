from app.interaction import engine


ids = [ "0" ]

config = {
    # 'type': 'incidents',
    'type': 'telegram',
    #'type': 'hatespeech',
    #'type': 'twitter',
    #'type': 'survey',
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

            if message[:3] == "p>>":
                engine.feedEnginePublic("0", message[3:])
            else: 
                engine.feedEnginePrivate("0", message)

        except KeyboardInterrupt:
            break