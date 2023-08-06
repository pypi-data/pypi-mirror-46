import os as _os

_PATH = _os.path.join(_os.path.expanduser("~"), ".local", ".py.syntax.autoimport")
if _os.path.isfile(_PATH):
    with open(_PATH) as _f:
        for _line in (_x for _x in _f.read().split("\n") if _x):
            _line = _line.strip()
            if " as " in _line:
                _alias = _line.split(" as ")[1].strip()
                _path = _line.split(" as ")[0].strip()
            else:
                _alias = _path = _line
            globals()[_alias] = __import__(_path)

def make_autoimport(*mods, **named):
    """
    This function shall be used to produce your autoimport list
    Pass modules as args to be imported by their qualified name
    and by kwargs to be imported aliased
    """
    text1 = "\n".join([x.__name__ for x in mods])
    text2 = "\n".join(["{} as {}".format(v.__name__, k) for k, v in named.items()])
    text = "{}\n{}".format(text1, text2)
    with open(_PATH, "w") as f:
        f.write(text)
