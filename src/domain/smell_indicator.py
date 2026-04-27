class SmellIndicator:
    def __init__(self, severity, description):
        self.severity = severity
        self.description = description

        self.smells = []

    def add_smell(self, smell):
        self.smells.append(smell)

    def __str__(self):
        return f"[{self.severity}] {self.description}"