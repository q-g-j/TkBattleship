class DependencyInjector:
    def __init__(self):
        self.__singletons = {}

    def resolve(self, cls):
        if cls in self.__singletons and self.__singletons[cls] is not None:
            return self.__singletons[cls]

        dependencies = [self.resolve(dep) for dep in getattr(cls, '__dependencies__', [])]
        instance = cls(*dependencies)
        self.__singletons[cls] = instance
        return instance

    def add_singleton(self, cls):
        self.__singletons[cls] = None

    def register_instance(self, instance):
        if instance.__class__ not in self.__singletons:
            self.__singletons[instance.__class__] = instance


def inject(*dependencies):
    def decorator(cls):
        setattr(cls, '__dependencies__', dependencies)
        return cls

    return decorator
