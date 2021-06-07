# This function asks if we want to continue and prints a custom message
def prompt_continue(message):
    prompt = "j/n: "
    print(f"{message}")
    return  input(prompt).upper() in ["J", "Y", "JA", "YES"]

# This function asks us to choose from a list of options
def prompt_option(message, options, nota = False):
    selected = None

    if nota and "None of these!" not in options:
        options.append("None of these!")

    print(f"{message}")
    print(f"Options:")
    for i, opt in enumerate(options):
        print(f"\t{i+1}). {opt}")

    prompt = f"1-{len(options)}: "
    ret = input(prompt)

    try:
        selected = options[int(ret)-1]
    except IndexError:
        selected = None
    except ValueError:
        if ret in options:
            selected = ret

    if selected:
        print(f"You chose '{selected}'.")  
    else:
        print(f"Selection not understood!")  

    if nota and selected == "None of these!":
        selected = None
        
    return selected


   # This function asks us to choose from a list of options
def prompt_rating(message):
    selected = None
    rating = None

    print(f"{message}")

    ret = input("Rating [0-10]: ")
    try:
        rating = float(ret)

        if rating < 0.0 or rating > 10.0:
            raise ValueError
    except ValueError:
        print("Rating not understood")

    return rating