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

        print("total time taken: " + str(self.totalTime), end="")

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


    def customSort(self, maxValue, listToSort):
        """
        My custom sort that uses counting sort on values 10000 and under,
        then uses merge sort on the rest of the values. This is to account
        for the skewed distribution where 98% of players have less than a
        total of 10000 xp.
        :param maxValue: the max value we will count sort
        :param listToSort: the list we want to sort
        :return: return the sorted list
        """
        unsortedForMergeSort = []
        sortedMergeSort = []

        sortedList = self.countingSort(listToSort, maxValue)

        # get a list of anything over max value
        for val in listToSort:
            if val > maxValue:
                unsortedForMergeSort.append(val)

        # MERGE SORT
        sortedMergeSort = self.mergeSort(maxValue, unsortedForMergeSort)

        # Combine for the final list and return
        finalList = sortedList + sortedMergeSort
        return finalList


    def countingSort(self, listToSort, maxValue):
        """
        Implementation of counting sort
        :param listToSort: the list we want to sort
        :param maxValue: the max value we will count sort
        :return: return the sorted list
        """
        sortedList = []
        counts = [0] * (maxValue + 1)

        # build the list of counts from the list we want sorted
        for i in range(len(listToSort)):
            # if the value is below our threshold, include it
            if (listToSort[i] <= maxValue):
                counts[listToSort[i]] += 1

        # convert list of counts back to list of integers
        for i in range(maxValue):
            while (counts[i] > 0):
                counts[i] -= 1
                sortedList.append(i)

        return sortedList

    def mergeSort(self, maxValue, listToSort):
        """
        Function that merge sorts a list of numbers. Referenced the CS450 slides for this implementation
        :param maxValue:
        :param listToSort: list we want to merge sort
        :return: return the sorted list
        """
        if len(listToSort) <= 1:
            return listToSort

        # do integer division
        midpoint = len(listToSort) // 2

        # Sort from the first element to the midpoint
        lHalf = self.mergeSort(maxValue, listToSort[0: midpoint])
        # sort from the midpoint to the end
        uHalf = self.mergeSort(maxValue, listToSort[midpoint:])

        # recombine the lists
        return self.mergeSortedLists(lHalf, uHalf)


    def mergeSortedLists(self, lHalf, uHalf):
        """
        Put the sorted lists back together
        :param lHalf: The lower list
        :param uHalf: The upper list
        :return: return the combined sorted list
        """
        result = []
        # indices of the next values to take from each list
        lowerIndex = 0
        upperIndex = 0

        # while there are still values
        while((lowerIndex < len(lHalf)) or (upperIndex < len(uHalf))):
            # if one of the lists is empty, add the rest of the other list to it and return it
            if(upperIndex >= len(uHalf)):
                return result + lHalf[lowerIndex:]
            if(lowerIndex >= len(lHalf)):
                return result + uHalf[upperIndex:]
            # add the lower values to the results
            if(lHalf[lowerIndex] <= uHalf[upperIndex]):
                result.append(lHalf[lowerIndex])
                lowerIndex += 1
            else:
                result.append(uHalf[upperIndex])
                upperIndex += 1

        return result


if __name__ == '__main__':
    # Runs the "standard" sort (Quick sort using Hoare's partitioning)
    if(len(sys.argv) == 1):
        print("Need to specify which sort you want to use ('custom' or 'standard).")
    else:
        if(sys.argv[1] == "standard"):
            print("Standard")
            data = Data()
            data.prepDataForSort()

            # Sort each skill
            for skill in data.allSkills:
                start_time = time.time_ns()
                data.hoaresQSort(0, len(skill) - 1, skill)
                time_taken_in_microseconds = (time.time_ns() - start_time) / 1000.0
                data.time.append(int(time_taken_in_microseconds))

            data.totalTime = sum(data.time)
            # print all skills to standard out
            data.printAllLists()

        elif(sys.argv[1] == "custom"):
            # Run the custom sort (combination of counting and merge sort)
            print("Custom")
            data = Data()
            data.prepDataForSort()

            # Sort each skill
            for i, skill in enumerate(data.allSkills):
                start_time = time.time_ns()
                data.allSkills[i] = data.customSort(10000, skill)
                time_taken_in_microseconds = (time.time_ns() - start_time) / 1000.0
                data.time.append(int(time_taken_in_microseconds))

            data.totalTime = sum(data.time)
            # print all skills to standard out
            data.printAllLists()


