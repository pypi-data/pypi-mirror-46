class Sleep360Error(Exception):

    def __init__(self, msg):
        self._submodule = None
        self._msg = msg

    def __init__(self, submodule, msg):
        self._submodule = submodule
        self._msg = msg

    def __str__(self):
        if self._submodule == None:
            return "sleep360: %s" % (self._msg)
        else:
            return "sleep360(%s): %s" % (self._submodule, self._msg)
