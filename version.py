class Version:
    def __init__(self, major=0, minor=0, micro=0):
        self.major = major
        self.minor = minor
        self.micro = micro

    def __str__(self):
        return '{}.{}.{}'.format(self.major, self.minor, self.micro)


VER = Version(0, 2, 0)
