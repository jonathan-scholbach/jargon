from os.path import basename, splitext


def __title(s):
    return " ".join([part[0].upper() + part[1:] for part in s.split()])


def title_from_path(file_path: str):
    path = splitext(file_path)[0]
    path = path[:-1] if path[-1] == "/" else path

    return __title(
        basename(path).split("__")[-1].replace("_", " ")  # throw away prefix
    )
