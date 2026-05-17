class Dependency:

    def __init__(
        self,
        name,
        version,
        dep_type,
        source,
        purl=None
    ):
        self.name = name
        self.version = version
        self.dep_type = dep_type
        self.source = source
        self.purl = purl

        self.smell_indicators = []

    def add_smell_indicator(self, smell):
        self.smell_indicators.append(smell)

    def has_smells(self):
        return len(self.smell_indicators) > 0