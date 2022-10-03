import sys
import time


class Data:
    def __init__(self):
        self.lines = []
        self.data2D = []
        self.categories = ["SKILL_BREAKDANCING", "SKILL_APICULTURE", "SKILL_BASKET",
                           "SKILL_XBASKET", "SKILL_SWORD", "TOTAL_XP"]
        self.breakDancingOut = []
        self.apicultureOut = []
        self.basketOut = []
        self.xBasketOut = []
        self.swordOut = []
        self.totalXpOut = []

        self.time = []
        self.totalTime = 0

        self.allSkills = [self.breakDancingOut, self.apicultureOut, self.basketOut,
                          self.xBasketOut, self.swordOut, self.totalXpOut]

    def printAllLists(self):
        """
        Print all lists to standard out
        :return:
        """
        for i, curList in enumerate(self.allSkills):
            print(self.categories[i])
            for entry in curList[::-1]:
                print(str(entry))
            print("time taken: " + str(self.time[i]) + "\n")

        print("total time taken: " + str(self.totalTime))

    def printAllListsToFile(self):
        """
        Will edit to print lists to a file
        """
        with open("testOut", "w+") as file:
            # for each skill
            for i, curList in enumerate(self.allSkills):
                # output the skill name
                file.write(self.categories[i] + "\n")
                for entry in curList[::-1]:
                    # output the values
                    file.write(str(entry) + "\n")
                file.write("time taken: " + str(self.time[i]) + "\n\n")

            file.write("total time taken: " + str(self.totalTime))
            # file.close()

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
        for line in sys.stdin:
            self.lines.append(line)

    def stripEndlines(self):
        """
        Remove all \n
        """
        for i, line in enumerate(self.lines):
            curLine = self.lines[i].rstrip()  # remove everything that is whitespace at the end of the line
            self.lines[i] = curLine

    def turnLinesTo2DList(self):
        """
        Fill out a 2D list with all the data
        Makes it easier to parse
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


    def fillOutAllSkills(self):
        for line in self.lines:
            if line:
                numbers = [int(num) for num in line.split() if num.isdigit()]
                self.allSkills[0].append(numbers[0])
                self.allSkills[1].append(numbers[1])
                self.allSkills[2].append(numbers[2])
                self.allSkills[3].append(numbers[3])
                self.allSkills[4].append(numbers[4])
                self.totalXpOut.append((sum(numbers)))


    def turn2DToSepLists(self):
        """
        Add all data to its respective lists
        """
        for row in self.data2D:
            for i, val in enumerate(row):
                self.allSkills[i].append(val)


    def prepDataForSort(self):
        """
        Get the data into the 2D list and add the total xp column
        It is now ready for sorting
        """
        self.readFromStdIn()
        self.stripEndlines()
        # self.turnLinesTo2DList()
        self.fillOutAllSkills()

    def hoaresQSort(self, low, high, listToSort):
        if(low < high):
            partition = self.hoaresPartition(low, high, listToSort)

            self.hoaresQSort(low, partition, listToSort)
            self.hoaresQSort(partition + 1, high, listToSort)




    def hoaresPartition(self, low, high, listToSort):
        piv = listToSort[(high+low) // 2]
        left = low - 1
        right = high + 1

        while(True):
            left += 1
            while(listToSort[left] < piv):
                left += 1
            right -= 1
            while(listToSort[right] > piv):
                right -= 1
            if left >= right:
                return right
            listToSort[left], listToSort[right] = listToSort[right], listToSort[left]


    def countingSort(self, maxValue, listToSort):
        sorted = []
        unsortedForMergeSort = []
        sortedMergeSort = []
        counts = [0] * (maxValue+1)

        for i in range(len(listToSort)):
            if(listToSort[i] <= maxValue):
                counts[listToSort[i]] += 1

        for i in range(maxValue):
            while(counts[i] > 0):
                counts[i] -= 1
                sorted.append(i)

        # get a list of anything over max value
        for val in listToSort:
            if val > maxValue:
                unsortedForMergeSort.append(val)

        sortedMergeSort = self.mergeSort(maxValue, unsortedForMergeSort)

        finalList = sorted + sortedMergeSort
        return finalList

        # print(sorted)

        # MERGE SORT

        # save off counting sort list
        # Then merge sort everything above maxVal in counting sort
        # then combine two lists again

    def mergeSort(self, maxValue, listToSort):
        if len(listToSort) <= 1:
            return listToSort

        midpoint = len(listToSort) // 2

        lHalf = self.mergeSort(maxValue, listToSort[0: midpoint])
        uHalf = self.mergeSort(maxValue, listToSort[midpoint:])

        return self.mergeSortedLists(lHalf, uHalf)


    def mergeSortedLists(self, lHalf, uHalf):
        result = []
        lowerIndex = 0
        upperIndex = 0

        while((lowerIndex < len(lHalf)) or (upperIndex < len(uHalf))):
            if(upperIndex >= len(uHalf)):
                return result + lHalf[lowerIndex:]
            if(lowerIndex >= len(lHalf)):
                return result + uHalf[upperIndex:]
            if(lHalf[lowerIndex] <= uHalf[upperIndex]):
                result.append(lHalf[lowerIndex])
                lowerIndex += 1
            else:
                result.append(uHalf[upperIndex])
                upperIndex += 1

        return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # whichSort = ""
    # if(whichSort == "standard"):
    #     print("Standard")
    # elif(whichSort == "custom"):
    #     print("Custom")
    #     data = Data()
    #     data.prepDataForSort()
    #
    #     # turn data back to list
    #     data.turn2DToSepLists()
    #     data.printAllLists()

# ===================================================
#     data = Data()
#     data.prepDataForSort()
#     # listToSort = data.allSkills[0]
#
#     for skill in data.allSkills:
#         start_time = time.time_ns()
#         data.hoaresQSort(0, len(skill) - 1, skill)
#         time_taken_in_microseconds = (time.time_ns() - start_time) / 1000.0
#         data.time.append(time_taken_in_microseconds)
#         # file = open("testOut", "w")
#         # file.write("time taken: " + str(time_taken_in_microseconds))
#     data.totalTime = sum(data.time)
#     data.printAllLists()
# ===================================================

    data = Data()
    data.prepDataForSort()
    # data.countingSort(10000, data.allSkills[0])
    # helpMe = data.mergeSort(10000, data.allSkills[0])
    data.allSkills[0] = data.countingSort(10000, data.allSkills[0])
    print(data.allSkills[0])


    # data.hoaresQSort(0, len(data.allSkills[0]) - 1, data.allSkills[0])
    # data.hoaresQSort(0, len(data.allSkills[1]) - 1, data.allSkills[1])
    # data.hoaresQSort(0, len(data.allSkills[2]) - 1, data.allSkills[2])
    # data.hoaresQSort(0, len(data.allSkills[3]) - 1, data.allSkills[3])
    # data.hoaresQSort(0, len(data.allSkills[4]) - 1, data.allSkills[4])
    # data.hoaresQSort(0, len(data.allSkills[5]) - 1, data.allSkills[5])

    # data.fillOutAllSkills()

    # turn data back to list
    # data.turn2DToSepLists()
    # data.printAllLists()
    # data.printAllListsToFile()

