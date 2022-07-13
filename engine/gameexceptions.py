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


class DataManagerException(Exception):

    def __init__(self, message=None):
        if message:
            super().__init__(message)
        else:
            super().__init__()


class FileNotFound(DataManagerException):
    _message = 'File not in files dictionnary of data manager (path not set). '

    def __init__(self, filename=None):
        if filename:
            super().__init__(FileNotFound._message+str(filename))
        else:
            super().__init__(FileNotFound._message)


class DirectoryNonExistent(DataManagerException):
    _message = "Directory not found. Process stopped"

    def __init__(self, dirname=None):
        if dirname:
            super().__init__(DirectoryNonExistent._message + dirname)
        else:
            super().__init__(DirectoryNonExistent._message)