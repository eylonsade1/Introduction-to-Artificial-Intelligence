class SingletonDeclaration(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance[cls] = super(SingletonDeclaration,cls).__call__(cls, *args, **kwargs)
        return cls._instance

class Singleton(metaclass=SingletonDeclaration):
    pass