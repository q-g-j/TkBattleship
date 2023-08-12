class DependencyInjector:
    def __init__(self):
        self.__singletons = {}
        self.__transients = []

    def resolve(self, cls):
        is_singleton = cls in self.__singletons

        if not is_singleton and cls not in self.__transients:
            raise Exception("'{0}' is not a registered type".format(cls))

        if is_singleton and self.__singletons[cls] is not None:
            return self.__singletons[cls]

        dependencies = [self.resolve(dep) for dep in getattr(cls, '__dependencies__', [])]
        instance = cls(*dependencies)
        if is_singleton:
            self.__singletons[cls] = instance
        print(cls)
        return instance

    def add_singleton(self, cls):
        if cls in self.__singletons:
            raise Exception("'{0}' already registered as a singleton object.".format(cls))
        self.__singletons[cls] = None

    def add_transient(self, cls):
        if cls in self.__singletons:
            raise Exception("'{0}' already registered as a transient object.".format(cls))
        self.__transients.append(cls)

    def register_instance(self, instance):
        if instance.__class__ in self.__singletons:
            raise Exception("'{0}' already registered as a singleton object.".format(instance.__class__))
        self.__singletons[instance.__class__] = instance

    def unregister(self, cls):
        is_singleton = cls in self.__singletons
        is_transient = cls in self.__transients
        if not is_singleton and not is_transient:
            raise Exception("'{0}' is not a registered type".format(cls))
        if is_singleton:
            del self.__singletons[cls]
        else:
            self.__transients.remove(cls)


def inject(*dependencies):
    def decorator(cls):
        setattr(cls, '__dependencies__', dependencies)
        return cls

    return decorator
