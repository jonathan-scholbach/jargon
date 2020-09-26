COLORS = {
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "magenta": 5,
    "cyan": 6,
    "white": 7,
}


def cprint(s: str, color: str = "white"):
    print(f"\33[3{COLORS[color]}m{s}\33[37m")
