class a:
    def __init__(self, dlina):
        self.dlina_a = dlina
        self.price = 4
class b(a):
    def __init__(self, dlina):
        super().__init__(dlina)
        print(self.price)

test = b(3)