class Attack:
    def __init__(self, name, description, impact):
        self.name = name
        self.description = description
        self.impact = impact

    def __str__(self):
        return self.name