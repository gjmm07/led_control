from define_leds import LED


class LEDArray:
    def __init__(self, file):
        self.array = []
        row_index, row = 0, []
        with open(file, "r") as f:
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

    def __setitem__(self, key, value):
        """ Converts the given key to a slice and switches the corresponding LED in a given color on or off"""
        rows = key[0] if type(key[0]) != int else slice(key[0], key[0]+1)
        cols = key[1] if type(key[1]) != int else slice(key[1], key[1]+1)
        state, color = value
        for row in self.array[rows]:
            for led in row[cols]:
                led.change_state(state, color)
        # [[led.change_state(value[0], value[1]) for led in r[cols]] for r in self.array[rows]]

    def return_state_array(self):
        """ Returns an array with the current led state"""
        return [[x.state for x in self.array[i]] for i in range(len(self.array))]

    def print_color_array(self):
        """ Prints the color of the LED Array. If a specific LED state is off an x will be printed """
        [print([x.color.ljust(8) if x.state else "x".ljust(8) for x in self.array[i]]) for i in range(len(self.array))]

    def rain(self):
        print("hello")

    def sideways(self):
        print("sidways")


if __name__ == "__main__":
    mat = LEDArray("led_data.txt")
    mat[1, 1] = True, "Red"
    mat[0, :] = True, "Blue"
    print(mat.return_state_array())
