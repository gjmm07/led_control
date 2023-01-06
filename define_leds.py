class LED:
    def __init__(self, name, gpio_pin, identi):
        self.name = name
        self.gpio_pin = gpio_pin
        self.color = "White"
        self.state = False
        self.id = identi

    def change_state(self, state, color):
        self.state = state
        self.color = color


