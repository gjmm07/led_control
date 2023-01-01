from define_leds import LED


class LEDArray:
    def __init__(self):
        self.array = []

    def insert(self, place, led):
        self.array[place[0]][place[1]][1] = led

    def display_array_state(self):
        for row in self.array:
            print(row[0])

    def read_from_file(self):
        row_index = 0
        row = []
        with open("led_data.txt", "r") as f:
            for line in f.readlines():
                d = dict.fromkeys(["gpio", "id"], 0)
                for item in line.split(","):
                    name, spec = item.strip().split(":")
                    if name == "row":
                        new_row_index = int(spec)
                        if new_row_index != row_index:
                            self.array.insert(new_row_index, row)
                            row = []
                            row_index = new_row_index
                    else:
                        d[name] = int(spec)
                row.append(LED(name="A", gpio_pin=d["gpio"], identi=d["id"]))
            self.array.append(row)

    def turn_on_row(self, row):
        [led.set_state(True) for led in self.array[row]]

    def turn_on_col(self, col):
        [led[col].set_state(True) for led in self.array]

    def update_led_array(self):
        return [[x.state for x in self.array[i]] for i in range(len(self.array))]


if __name__ == "__main__":
    m = LEDArray()
    m.read_from_file()
