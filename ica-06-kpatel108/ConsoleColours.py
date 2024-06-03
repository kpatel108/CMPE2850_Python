#https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class ConsoleColors:
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'
#Only portion ConsoleColors for demo purposes

msg = "Check Check Check"
#Red-background AND White-foreground set - now all text will adopt that scheme
print( ConsoleColors.CREDBG + ConsoleColors.CWHITE + f"{msg:80}")
print( "OOPs, still on, turning off" + ConsoleColors.CEND )
print( "Colors off..")