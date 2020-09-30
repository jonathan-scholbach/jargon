from os import system, name


def clear():
    if name == "nt":  # for windows
        _ = system("cls")
    else:
        _ = system("clear")

    print("\n")