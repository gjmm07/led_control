from LED_array import LEDArray

#
# LED Steuerung Eike
#

# define constants
mat = LEDArray()
mat.read_from_file()
ARRAY_SIZE = mat.return_size()
COLORS = ("RED", "BLUE", "GREEN")


class MenuObject:
    def __init__(self, name, slaves, last=False):
        self.name = name
        self.slaves = slaves
        self.last = last

    def return_slaves_name(self):
        if not self.last:
            return [i.name for i in self.slaves]
        return self.slaves

    def return_slave(self, name):
        for i in self.slaves:
            if i.name == name:
                return i


row = {"ROW": ["1", "2", "3"]}
column = {"Column": ["1", "2", "3"]}
color = {"COLOR": ["RED", "BLUE", "GREEN"]}

select_all = MenuObject(name="SELECT ALL", slaves=color, last=True)
select_single = MenuObject(name="SELECT SINGLE", slaves=(row | column | color), last=True)
select_row = MenuObject(name="SELECT ROW", slaves=(row | color), last=True)
select_column = MenuObject(name="SELECT COLUMN", slaves=(column | color), last=True)
static = MenuObject(name="STATIC", slaves=(select_column, select_row, select_single, select_all))

select_rain = MenuObject(name="SELECT RAIN", slaves=None, last=True)
select_sideways = MenuObject("SELECT SIDEWAYS", slaves=None, last=True)
dynamic = MenuObject(name="DYNAMIC", slaves=(select_rain, select_sideways))

main_menu = MenuObject(name="MAIN MENU", slaves=(dynamic, static))


def menu(master_order):
    while True:
        master = master_order[-1]
        if not master.last:
            selection = button_select(master.return_slaves_name(), [x.name for x in master_order])
            master_order.append(master.return_slave(selection))
        else:
            selection = dict.fromkeys(master.slaves.keys(), None)
            for key, attribute in master.slaves.items():
                selection[key] = button_select(header=key, items=attribute)
            master_order = yield master_order[-1].name, selection
        menu(master_order)


def main():
    a = menu([main_menu])
    name, sel = next(a)
    while True:
        print(name, sel)
        name, sel = a.send([main_menu])


def turn_on_row():
    print("turn on row")


def button_select(items, header):
    print("\n")
    print(header)
    while True:
        selection = input("Please select from the following {}: ".format(items))
        if selection.upper() in str(items):
            return selection.upper()
        elif selection.upper() == "BACK":
            return "BACK"


if __name__ == "__main__":
    main()
