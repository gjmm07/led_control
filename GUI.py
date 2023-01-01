from LED_array import LEDArray
#
# LED Steuerung Eike
#

# define constants
mat = LEDArray()
mat.read_from_file()
ARRAY_SIZE = 3, 3
COLORS = ["Red", "Blue", "Green"]
MAIN_MENU_OBJ = {"Static": {"All": {"Color": dict.fromkeys(COLORS, None)},
                            "Row": {"Row": dict.fromkeys([str(i) for i in range(ARRAY_SIZE[0])], None),
                                    "Color": dict.fromkeys(COLORS, None)},
                            "Column": {"Column": dict.fromkeys([str(i) for i in range(ARRAY_SIZE[1])], None),
                                       "Color": dict.fromkeys(COLORS, None)},
                            "Single": {"Row": dict.fromkeys([str(i) for i in range(ARRAY_SIZE[0])], None),
                                       "Column": dict.fromkeys([str(i) for i in range(ARRAY_SIZE[1])], None),
                                       "Color": dict.fromkeys(COLORS, None)}},
                 "Dynamic": {"Rain": None,
                             "Sideways": None},
                 "Sleep": None}


class MenuObject:
    def __init__(self, name, slaves, last=False):
        self.name = name
        self.slaves = slaves
        self.last = last

    def return_slaves_name(self):
        return [i.name for i in self.slaves]

    def return_slave(self, name):
        for i in self.slaves:
            if i.name == name:
                return i


row = MenuObject(name="ROW", slaves=("a", "b"), last=True)
column = MenuObject(name="COLUMN", slaves=("a", "b"), last=True)
color = MenuObject(name="COLOR", slaves=("a", "b"), last=True)

select_all = MenuObject(name="SELECT ALL", slaves=color)
select_single = MenuObject(name="SELECT SINGLE", slaves=(row, column, color))
select_row = MenuObject(name="SELECT ROW", slaves=(row, color))
select_column = MenuObject(name="SELECT COLUMN", slaves=(column, color))
static = MenuObject(name="STATIC", slaves=(select_column, select_row, select_single, select_all))

select_rain = MenuObject(name="SELECT RAIN", slaves=None, last=True)
select_sideways = MenuObject("SELECT SIDEWAYS", slaves=None, last=True)
dynamic = MenuObject(name="DYNAMIC", slaves=(select_rain, select_sideways))

main_menu = MenuObject(name="MAIN MENU", slaves=(dynamic, static))


def menu(master_order):
    master = master_order[-1]
    if not master.last:
        selection = button_select(master.return_slaves_name())
        master_order.append(master.return_slave(selection))
        menu(master_order)
    else:
        print("reached")


def turn_on_row():
    print("turn on row")


def button_select(items):
    while True:
        selection = input("Please select from the following {}: ".format(items))
        if selection.upper() in str(items):
            return selection.upper()


if __name__ == "__main__":
    menu([main_menu])

