import random as rnd
from Bars import Bars, ColorBar, ValueBar, BarManager
from ConsoleColours import ConsoleColors

descriptions = ['Mars','Earth','Saturn','Jupiter','Asteroid','Radiation','Intergalactic','Alpha Centauri']

def bar_test():
    print("Value Bar Test")
    print("[0")
    print("[1]")

    for x in range(10, 120, 10):
        print(ValueBar(x, rnd.choice(descriptions), ConsoleColors.CBLACK, ConsoleColors.CREDBG).draw("\u2588"))
        print(ValueBar(x + 1, rnd.choice(descriptions), ConsoleColors.CBLACK, ConsoleColors.CBLUEBG).draw("\u2588"))


# Create a ManagerTest function.
# Using desc_list
# for some descriptions, create a mix of valid bars ensuring some duplicate values exist.
# Generate test to produce the output as shown below.
def manager_test():
    print("\n")
    print("Manager Test")

    barManager = BarManager()

    barManager.addBar(Bars(10, rnd.choice(descriptions)))
    barManager.addBar(Bars(50, rnd.choice(descriptions)))
    barManager.addBar(ValueBar(12, rnd.choice(descriptions), ConsoleColors.CBOLD, ConsoleColors.CREDBG))
    barManager.addBar(ColorBar(25, rnd.choice(descriptions)))
    barManager.addBar(ColorBar(255, rnd.choice(descriptions)))
    barManager.addBar(ValueBar(11, rnd.choice(descriptions), ConsoleColors.CBOLD, ConsoleColors.CREDBG))
    barManager.addBar(ColorBar(25, rnd.choice(descriptions)))
    barManager.addBar(ValueBar(11, rnd.choice(descriptions), ConsoleColors.CBOLD, ConsoleColors.CREDBG))
    barManager.addBar(ValueBar(50, rnd.choice(descriptions)))
    barManager.addBar(ValueBar(100, rnd.choice(descriptions)))
    barManager.addBar(Bars(20, rnd.choice(descriptions)))
    barManager.addBar(ColorBar(15, rnd.choice(descriptions)))
    barManager.addBar(ColorBar(85, rnd.choice(descriptions)))
    barManager.addBar(ColorBar(10, rnd.choice(descriptions)))
    barManager.addBar(ValueBar(30, rnd.choice(descriptions), ConsoleColors.CRED, ConsoleColors.CGREENBG))
    barManager.addBar(ValueBar(80, rnd.choice(descriptions), ConsoleColors.CBOLD, ConsoleColors.CYELLOWBG))
    barManager.addBar(ValueBar(85, rnd.choice(descriptions), ConsoleColors.CGREEN, ConsoleColors.CBLUEBG))
    barManager.addBar(ValueBar(32, rnd.choice(descriptions)))

    # removing bars
    barManager.remove_bar(32)
    barManager.remove_bar(10)

    # sorting the bar
    barManager.sort_bars()

    # show the bars
    barManager.draw_bars()