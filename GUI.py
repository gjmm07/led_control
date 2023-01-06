from LED_array import LEDArray
import _thread

#
# LED Steuerung Eike
#

# define constants
COLORS = ("RED", "BLUE", "GREEN")
mat = LEDArray("led_data.txt")


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


row = {"ROW": ["0", "1", "2"]}
column = {"COLUMN": ["0", "1", "2"]}
color = {"COLOR": ["RED", "BLUE", "GREEN"]}
state = {"STATE": ["ON", "OFF"]}
frequency = {"FREQUENCY": ["FAST", "MODERATE", "SLOW"]}

select_all = MenuObject(name="SELECT ALL", slaves=(color | state), last=True)
select_single = MenuObject(name="SELECT SINGLE", slaves=(row | column | color | state), last=True)
select_row = MenuObject(name="SELECT ROW", slaves=(row | color | state), last=True)
select_column = MenuObject(name="SELECT COLUMN", slaves=(column | color | state), last=True)
static = MenuObject(name="STATIC", slaves=(select_column, select_row, select_single, select_all))

select_rain = MenuObject(name="SELECT RAIN", slaves=(color | frequency | state), last=True)
select_sideways = MenuObject("SELECT SIDEWAYS", slaves=None, last=True)
dynamic = MenuObject(name="DYNAMIC", slaves=(select_rain, select_sideways))

main_menu = MenuObject(name="MAIN MENU", slaves=(dynamic, static))


def menu(master_order):
    while True:
        master = master_order[-1]
        if not master.last:
            selection = button_select(master.return_slaves_name() + ["BACK"], [x.name for x in master_order])
            if selection == "BACK":
                if len(master_order) > 1:
                    del master_order[-1]
            else:
                master_order.append(master.return_slave(selection))
        else:
            selection = dict.fromkeys(master.slaves.keys(), None)
            for key, attribute in master.slaves.items():
                selection[key] = button_select(header=[x.name for x in master_order] + [key], items=attribute)
            master_order = yield master_order, selection
        menu(master_order)


def main():
    a = menu([main_menu])
    order, sel = next(a)
    while True:
        top_name, name = order[1].name, order[-1].name
        print(top_name)
        if top_name == "STATIC":
            sel["STATE"] = sel["STATE"] == "ON"
            if name == "SELECT ROW":
                mat[int(sel.get("ROW")), :] = sel.get("STATE"), sel.get("COLOR")
            elif name == "SELECT COLUMN":
                mat[:, int(sel.get("COLUMN"))] = sel.get("STATE"), sel.get("COLOR")
            elif name == "SELECT ALL":
                mat[:, :] = sel.get("STATE"), sel.get("COLOR")
            elif name == "SELECT SINGLE":
                mat[int(sel.get("ROW")), int(sel.get("COLUMN"))] = sel.get("STATE"), sel.get("COLOR")
            mat.print_color_array()
        elif top_name == "DYNAMIC":
            dict_ = dict(zip(order[1].return_slaves_name(), [mat.rain, mat.sideways]))
            dict_[name]()
        order, sel = a.send([main_menu])


def button_select(items, header):
    print(header)
    while True:
        selection = input("Please select from the following {}: ".format(items[:-1] if items[-1] == "BACK" else items))
        print("\n")
        if selection.upper() in str(items):
            return selection.upper()


if __name__ == "__main__":
    main()
