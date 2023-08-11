class DependencyInjector:
    def __init__(self):
        self.dependencies = {}

    def register(self, key, dependency):
        self.dependencies[key] = dependency

    def resolve(self, clazz):
        dependencies = [self.dependencies[dep] for dep in getattr(clazz, '__dependencies__', [])]
        return clazz(*dependencies)


def inject(*dependencies):
    def decorator(cls):
        setattr(cls, '__dependencies__', dependencies)
        return cls

    return decorator
