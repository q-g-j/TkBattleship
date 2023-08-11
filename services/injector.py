class DependencyInjector2:
    def __init__(self):
        self.dependencies = {}

    def register(self, key, dependency):
        self.dependencies[key] = dependency

    def resolve(self, clazz):
        dependencies = [self.dependencies[dep] for dep in getattr(clazz, '__dependencies__', [])]
        return clazz(*dependencies)


class DependencyInjector:
    def __init__(self):
        self.dependencies = {}

    def register(self, key, dependency):
        self.dependencies[key] = dependency

    def resolve(self, clazz):
        if clazz.__name__ in self.dependencies:
            return self.dependencies[clazz.__name__]
        dependencies = [self.dependencies[dep] for dep in getattr(clazz, '__dependencies__', [])]
        instance = clazz(*dependencies)
        self.dependencies[clazz.__name__] = instance
        return instance



def inject(*dependencies):
    def decorator(cls):
        setattr(cls, '__dependencies__', dependencies)
        return cls

    return decorator