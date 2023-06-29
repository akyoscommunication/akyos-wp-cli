import os


initialized = False


def initialize():
    global initialized

    if not initialized:
        os.system("")
        initialized = True


def getFormatCodes():
    formatCodes = {

        "&c": "9",  # Red
        "&4": "1",  # Dark Red
        "&6": "208",  # Orange
        "&e": "227",  # Yellow
        "&2": "34",  # Dark Green
        "&a": "47",  # Green
        "&b": "38",  # Aqua
        "&3": "33",  # Dark Aqua
        "&1": "21",  # Dark Blue
        "&9": "4",  # Blue
        "&d": "99",  # Light Purple
        "&5": "93",  # Purple
        "&f": "255",  # White
        "&7": "238",  # Gray
        "&8": "235",  # Dark Gray
        "&0": "232",  # Black

    }

    return formatCodes


def formatColor(colorCode):
    return getFormatCodes()[colorCode]


def color(text, reset=True) -> str:
    '''
    Color python text using Minecraft color code
    Exemple : color("&cThis is light red")
    You can also use multiple color code
    Exemple : color("&7S&8h&7a&8d&7o&8w")
    To use & symbol normally, use $_ instead
    '''

    initialize()

    colorFormatIndexes = searchWord("&", text)

    color = lambda text, color: "\33[38;5;" + str(color) + "m" + text
    if reset:
        color = lambda text, color: "\33[38;5;" + str(color) + "m" + text + "\33[0m"

    final_text = ""
    loop = 1

    for index in colorFormatIndexes:
        if str(text[index] + text[index + 1]) in getFormatCodes().keys():
            if loop != len(colorFormatIndexes):
                colored_text = text[index:colorFormatIndexes[loop]][2:]
            else:
                colored_text = text[index:len(text)][2:]
            final_text += color(colored_text, formatColor(str(text[index] + text[index + 1])))
        loop += 1

    return final_text.replace('$_', '&')


# =====================================================================================================

def printAllColors():
    initialize()

    fg = lambda text, color: "\33[38;5;" + str(color) + "m" + text + "\33[0m"
    bg = lambda text, color: "\33[48;5;" + str(color) + "m" + text + "\33[0m"

    def print_six(row, format, end="\n"):
        for col in range(6):
            color = row * 6 + col - 2
            if color >= 0:
                text = "{:3d}".format(color)
                print(format(text, color), end=" ")
            else:
                print(end="    ")  # four spaces
        print(end=end)

    for row in range(0, 43):
        print_six(row, fg, " ")
        print_six(row, bg)


# =====================================================================================================

def searchWord(searchQuery, searchInput):
    index = 0
    searchIndex = 0
    currentSearchState = ""
    currentSearchQuery = ""

    results = []

    for letter in searchInput:

        searchIndex += 1

        if letter == searchQuery[0] and index == 0:
            index += 1
            currentSearchState += letter
            if len(searchQuery) == 1:
                indexResult = searchIndex - len(searchQuery)
                results.append(indexResult)
                index = 0

        elif letter == searchQuery[index] and index != 0:
            index += 1
            currentSearchState += letter
            if currentSearchState == searchQuery:
                indexResult = searchIndex - len(searchQuery)
                results.append(indexResult)
                index = 0

        elif letter != searchQuery[index] and index != 0:
            index = 0
            currentSearchState = ""

    return results


if __name__ == "__main__":
    testText = color("&7test &btest &8test &atest")
    print(testText)
