class Error(Exception):
    def __init__(self, mssg):
        super().__init__(mssg)

    def __str__(self):
        return repr(self.mssg)

class NoInputForProcessing(Error):
    def __init__(self, mssg):
        super().__init__(mssg)

class InputOverloadForProcessing(Error):
    def __init__(self, mssg):
        super().__init__(mssg)

class UrlContentNotAccessible(Error):
    def __init__(self, mssg):
        super().__init__(mssg)
