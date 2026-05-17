class DependencyRepository:

    def save(self, dependency):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def find_by_name(self, name):
        raise NotImplementedError

    def exists(self, name, version, purl=None):
        raise NotImplementedError