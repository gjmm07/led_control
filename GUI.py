from LED_array import LEDArray

#
# LED Steuerung Eike
#

# define constants
mat = LEDArray()
mat.read_from_file()
ARRAY_SIZE = 3, 3
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


row = MenuObject(name="ROW", slaves=("A", "B"), last=True)
column = MenuObject(name="COLUMN", slaves=("A", "B"), last=True)
color = MenuObject(name="COLOR", slaves=COLORS, last=True)

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
    selection = ""
    while True:
        master = master_order[-1]
        selected_items = yield master.last, selection, master.slaves
        if not master.last:
            selection = button_select(master.return_slaves_name(), [x.name for x in master_order], selected_items)
            master_order.append(master.return_slave(selection))
        else:
            selection = button_select(master.return_slaves_name(), [x.name for x in master_order])
            del master_order[-1]
        menu(master_order)


def main():
    while True:
        first_over_last, input_, key = False, False, ""
        dict_ = {}
        a = menu([main_menu])
        next(a)
        while True:
            last, selection, slaves = a.send(dict_)
            if not first_over_last:
                if slaves[0].last:
                    dict_ = dict.fromkeys([s.name for s in slaves], [False, ""])
                    first_over_last = True
            else:
                if last:
                    input_, key = True, selection
                elif input_:
                    dict_[key] = [True, selection]
                    input_ = False
            if False not in [s[0] for s in list(dict_.values())] and dict_ != {}:
                print(dict_)
                break


def turn_on_row():
    print("turn on row")


def button_select(items, header, s=None):
    print("\n")
    print(header)
    if s != {} and s is not None:
        z = [item + "-d" if bool_ else item for item, bool_ in zip(items, [x[0] for x in list(s.values())])]
    else:
        z = items
    while True:
        selection = input("Please select from the following {}: ".format(z))
        if selection.upper() in str(items):
            return selection.upper()
        elif selection.upper() == "BACK":
            return "BACK"


if __name__ == "__main__":
    main()
