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
        if type(key[0]) == int and type(key[1]) == slice:
            [led.change_state(value[0], value[1]) for led in self.array[key[0]][key[1]]]
        elif type(key[0]) == slice and type(key[1]) == int:
            [led[key[1]].change_state(value[0], value[1]) for led in self.array[key[0]]]
        elif type(key[0]) == slice and type(key[1]) == slice:
            [[led.change_state(value[0], value[1]) for led in row[key[1]]] for row in self.array[key[0]]]
        else:
            self.array[key[0]][key[1]].change_state(value[0], value[1])

    def return_state_array(self):
        return [[x.state for x in self.array[i]] for i in range(len(self.array))]

    def print_color_array(self):
        [print([x.color if x.state else "x" for x in self.array[i]]) for i in range(len(self.array))]


if __name__ == "__main__":
    mat = LEDArray("led_data.txt")
    mat[1, 1] = True, "Red"
    mat[0:, ] = True, "Blue"
    print(mat.return_state_array())
    print(mat.return_color_array())
