class LED:
    def __init__(self, name, gpio_pin, identi):
        self.name = name
        self.gpio_pin = gpio_pin
        self.state = False
        self.id = identi

    def set_state(self, new_state):
        self.state = new_state

