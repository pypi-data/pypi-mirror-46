def say_dude(name=None):
    if name is None:
        return "Hello Dude"
    else:
        return "Hello, %s! (only None is Dude)" % name

