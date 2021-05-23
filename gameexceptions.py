class GameException(Exception):
    exceptiontypes = [
        'Error',
        'Warning',
    ]

    def __init__(self, exceptiontype):
        if exceptiontype not in GameException.exceptiontypes:
            raise GameException()
    
    
class EntityException(GameException):
    def __init__(self, entityid):
        super.__init__()