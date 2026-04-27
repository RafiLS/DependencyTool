class SupplyChainSmell:
    def __init__(self, name, smell_type, description):
        self.name = name
        self.type = smell_type
        self.description = description

        self.attacks = []

    def add_attack(self, attack):
        self.attacks.append(attack)

    def __str__(self):
        return self.name