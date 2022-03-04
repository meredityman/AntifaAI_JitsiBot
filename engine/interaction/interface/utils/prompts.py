import json

prompts = json.load(open("engine/config/errors.json", "r"))
NOTA   = prompts['none']
CHOOSE = prompts['choose']
ERROR  = prompts['error']

#This function asks if we want to continue and prints a custom message
def prompt_continue(message):
    prompt = "j/n: "
    print(f"{message}")
    return  input(prompt).upper() in ["J", "Y", "JA", "YES"]

# This function asks us to choose from a list of options
def prompt_option(message, options, nota = False):
    selected = None
    if nota and NOTA not in options:
        options.append(NOTA)

    try:
        selected = options[int(message)-1]
    except IndexError:
        selected = None
    except ValueError:
        if message in options:
            selected = message

    if selected is not None:
        response = CHOOSE.format(selected = selected)
    else:
        response = ERROR

    if nota and selected == NOTA:
        selected = None
        
    return selected, response

# This function asks us to choose from a list of options
def prompt_choice(message):
    selected = None

    _true = ['ja', 'j', 'yes', 'y', '1']
    _false = ['nein', 'n', 'no', '0']

    if message.lower() in _true:
        selected = True
    elif message.lower() in _false:
        selected = False

    if selected is not None:
        response = CHOOSE.format(selected = selected)
    else:
        response = ERROR 
        
    return selected, response

   # This function asks us to choose from a list of options
def prompt_rating(message, min, max):
    rating = None
    response = None
    try:
        rating = float(message)
        if rating < min or rating > max:
            raise ValueError
    except ValueError:
        response = ERROR
        rating = None


    return rating, response