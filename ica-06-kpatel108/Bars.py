import math


class Bars:
    _maxBarsVal = 0             # max of all bars
    _sumOfAllBars = 0           # accumulation of all current Bar values

    def __init__(self, barVal, barDesc):
        if (barVal < 0):
            raise ValueError('Val should be positive only');

        self.max_bars_val = barVal
        self.bar_desc = barDesc
        Bars._sumOfAllBars += barVal

        if (barVal > Bars._maxBarsVal):
            Bars._maxBarsVal = barVal


    def draw(self, histoChar='*', max_val = 1111):
        ret_str = ''
        histoWidth = round(self.max_bars_val / Bars._maxBarsVal * 100)      # convert to percent

        for x in range(0, histoWidth):
            ret_str += histoChar

        return ret_str




"""
class ColorBar derived from Bar. 
Supports a constructor with base class required arguments, and a foreground "color" selection.
It will support an override to Draw, but will prepend the foreground color code selection 
    and append the reset code to the result of the base Bar Draw invoke.
This should result in a colored bar being generated with a colored foreground fill character and returned.
"""
class ColorBar(Bars):       # inherited class from Bars
    def __init__(self, barVal, barDesc, foreCol = '\33[33m'):
        Bars.__init__(barVal, barDesc)      # explicit way of invoking base class CTOR, super() is recommended
        self.fore_col = foreCol

    def draw(self, histoChar='*', max_val = 1111):
        baseDrawStr = super().draw(histoChar)
        result = self.fore_col + baseDrawStr + '\33[0m'
        return result




"""
class ValueBar derived from Bar. 
Supports a constructor with base class required arguments, and a background and foreground color, 
    using a default background of white, and default foreground of black.

It will support an override to Draw, accepting ( but ignoring ) the fill character.
This will create a string of spaces, placing the actual value ( not percentage ) in the center.
This function must not use center() or any backspace characters or other cursor movement characters.
Just calculate the center, adjust for the value width and produce the string of spaces--value--spaces
    to fill the value width. Account for odd/even values to ensure your bar is exactly the correct
    width - put the extra space on the right. If there is NOT room for the value to fit in the calculated
    width, place the value to the right of the blocks/chars like : [value]
"""
class ValueBar(Bars):           # another class derived from Bars
    # default foreground colour = white, background colour = black
    def __init__(self, barVal, barDesc, foreCol = '\33[30m', backCol = '\33[47m'):
        super().__init__(barVal, barDesc)
        self.fore_col = foreCol
        self.back_col = backCol

    def draw(self, histoChar = '*', myMax= 111):
        barValStr = str(self.max_bars_val)
        barWidth = len(barValStr)       # for 100, it would be 3 digits
        histoValWidth = self.max_bars_val / myMax * 100
        bar_spaces = " " * (math.floor( histoValWidth / 2 ))
        spaces_2 = ""

        if (math.floor( histoValWidth ) % 2 == 1):
            spaces_2 = " "

        return self.fore_col + self.back_col + bar_spaces + barValStr + bar_spaces + spaces_2 + '\33[0m'




"""
class BarManager a Bar manager class, will maintain a collection of Bar objects. Add an instance member list of Bar in the CTOR.

We must make an assumption here - Since we use the Bar class member to maintain the maximum width, "old" Bar use will have set 
    the maximum -> corrupting new Bar additions - Therefore, a new BarManager will reset the Bar maximum back to 
    0 ( possibly breaking old Bars, but we will assume BarManagers will be used one at a time ). 
    Add the following methods :

    -> AddBar accepts and adds the supplied bar the collection.
    -> RemoveBar accepts a value and removes all bars from the collection that match that value. 
       Update the Bar class member if necessary ( was it the only maximum value )
    -> SortBars - sort the bars as description within descending value
    -> DrawBars - will print all the bars. Determine the longest description string of all current bars.
       Using that fixed width, output the description, followed by the return of each bar's Draw() method.
"""
class BarManager:
    def __init(self):
        self.bar_list = []
        Bars._maxBarsVal = 0        # reset the maximum limit

    def addBar(self, barList):
        self.bar_list = barList

    def remove_bar(self, removeVal):
        bars_to_remove = []
        max_bar = 0
        # find the bars to be removed and add it to the respective collection
        for item in self.bar_list:
            if item.barVal == removeVal:
                bars_to_remove.append(item)
            else:
                max_bar = max(max_bar, item.barVal)
        for item in bars_to_remove:
            self.bar_list.remove(item)

    def sort_bars(self):
        self.bar_list.sort(key=lambda x : x.bar_desc, reverse=True)

    def draw_bars(self, maxVal = 111):
        # find the longest desc string of all current bars
        long_desc = max( len(myBars.barDesc) for myBars in self.bar_list )
        # using the fixed longest desc width, output the desc and the bar using draw() method
        for item in self.bar_list:
            print(item.bar_desc.ljust(long_desc), " : ", item.draw("\u2588", maxVal))