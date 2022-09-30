import sys


class Data:
    def __init__(self):
        self.lines = []
        self.data2D = []
        self.categories = ["SKILL_BREAKDANCING", "SKILL_APICULTURE", "SKILL_BASKET",
                           "SKILL_XBASKET", "SKILL_SWORD", "TOTAL_XP"]
        self.breakDancingOut = ["SKILL_BREAKDANCING"]
        self.apicultureOut = ["SKILL_APICULTURE"]
        self.basketOut = ["SKILL_BASKET"]
        self.xBasketOut = ["SKILL_XBASKET"]
        self.swordOut = ["SKILL_SWORD"]
        self.totalXpOut = ["TOTAL_XP"]

        self.allSkills = [self.breakDancingOut, self.apicultureOut, self.basketOut,
                          self.xBasketOut, self.swordOut, self.totalXpOut]

    def printAllLists(self):
        """
        Print all lists to standard out
        :return:
        """
        for list in self.allSkills:
            for entry in list:
                print(entry)
            print("")

    def printAllListsToFile(self):
        """
        Will edit to print lists to a file
        :return:
        """
        for list in self.allSkills:
            for entry in list:
                print(entry)
            print("")

    def fileReader(self, filename):
        """
        Function reads the file, gets out all lines in the file
        :param filename: name of file as a string
        """
        file = open(filename, 'r')
        self.lines = file.readlines()
        for line in self.lines:
            print(line)
        file.close()

    def readFromStdIn(self):
        """
        Reads input from standard in and puts it in lines
        """
        readFirstLine = False
        for line in sys.stdin:
            if not readFirstLine:  # skip the first line (dimension)
                readFirstLine = True
                continue
            else:
                self.lines.append(line)

    def stripEndlines(self):
        """
        Remove all \n
        :return:
        """
        for i, line in enumerate(self.lines):
            curLine = self.lines[i].rstrip()  # remove everything that is whitespace at the end of the line
            self.lines[i] = curLine

    def turnLinesTo2DList(self):
        """
        Fill out a 2D list with all the data
        Makes it easier to parse
        :return:
        """
        for line in self.lines:  # loops over the rows
            if line:  # if line is an empty string, will skip over (evals to false)
                self.data2D.append(line.split(' '))

        self.data2D = [[int(val) for val in line] for line in self.data2D]

        # ADD THE TOTALXP COLUMN
        for row in self.data2D:
            total = 0
            for val in row:
                total += val
            row.append(total)

    def turn2DToSepLists(self):
        """
        Add all data to its respective lists
        :return:
        """
        for row in self.data2D:
            for i, val in enumerate(row):
                self.allSkills[i].append(val)

    # def readValuesToLists(self):


def standardQSort():
    print("This is quicksort")


def myQSort():
    print("This is Hoares Quicksort")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = Data()
    data.readFromStdIn()
    data.stripEndlines()
    data.turnLinesTo2DList()
    data.turn2DToSepLists()
    data.printAllLists()
    # print("WAAA")
