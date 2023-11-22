import datetime


class Node:
    def __init__(self, patronID, priorityNumber):
        self.patronID = patronID
        self.priorityNumber = priorityNumber
        self.timeOfReservation = datetime.datetime.now()


class ReservationHeap:
    def __init__(self, patronID, priorityNumber):
        node = Node(patronID, priorityNumber)
        self.heapSize = 1
        self.heap = [node]

    def hasParent(self, index):
        return index // 2 >= 0  # Checking whether the present node has a parent

    def getParent(self, index):
        if not self.hasParent(index):  # check if there is a parent and then get the parent
            return -1
        return self.heap[index // 2]

    def getParentIndex(self, index):  # If there is a parent then get the index of the parent
        if not self.hasParent(index):
            return -1
        return index // 2

    def hasRightChild(self, index):  # checking if there is right Child
        return (2 * index + 2) < self.heapSize

    def getRightChild(self, index):  # If there is right child then trying to get the right Child
        if not self.hasRightChild(index):
            return -1
        return self.heap[(2 * index + 2)]

    def getRightChildIndex(self, index):  # if there is right Child then get the Index
        if not self.hasRightChild(index):
            return -1
        return index * 2 + 2

    def hasLeftChild(self, index):  # Checking if there is left Child
        return (2 * index + 1) < self.heapSize

    def getLeftChild(self, index):  # if there is left child then tyring to get the leftChild
        if not self.hasLeftChild(index):
            return -1
        return self.heap[(2 * index + 1)]

    def getLeftChildIndex(self, index):  # if there is left Child then trying to get the index of the left Child
        if not self.hasLeftChild(index):
            return -1
        return 2 * index + 1

    def push(self, patronID, priorityNumber):  # Function to insert into the minHeap
        if self.heapSize >= 20:
            print("Wait list is Fill")
            return -1
        node = Node(patronID, priorityNumber)
        self.heapSize += 1
        self.heap.append(node)
        index = self.heapSize - 1
        while index != -1 and self.getParent(
                index) != -1:  # After each insert I am replacing the head with the minimum Priority patron
            if (self.heap[index].priorityNumber < self.heap[self.getParentIndex(index)].priorityNumber) or (
                    self.heap[index].timeOfReservation < self.heap[self.getParentIndex(index)].timeOfReservation and
                    self.heap[index].priorityNumber == self.heap[self.getParentIndex(index)].priorityNumber):
                self.heap[self.getParentIndex(index)], self.heap[index] = self.heap[index], self.heap[
                    self.getParentIndex(index)]
                index = self.getParentIndex(index)
            else:
                break
        return 0

    def removeMin(self):  # function to get the minimum from the heap
        if self.heapSize == 0:  # checking whether the heap is empty
            return -2
        elif self.heapSize == 1:  # checking if the heap has s1 element
            temp = self.heap[0]
            self.heapSize -= 1
            self.heap = []
            return temp
        temp = self.heap[
            0]  # If it has more than 1 then try to check the priority Number and then if there is tie using time of reserving the book the tie is breaked
        self.heap[0] = self.heap.pop(-1)
        self.heapSize -= 1
        index = 0
        while index != -1 and (self.getLeftChildIndex(index) != -1 or self.getRightChildIndex(index) != -1):
            if self.hasRightChild(index):  # checking if it has right Child
                if self.heap[index].priorityNumber > self.heap[self.getRightChildIndex(index)].priorityNumber and \
                        self.heap[self.getRightChildIndex(index)].priorityNumber < self.heap[
                    self.getLeftChildIndex(
                        index)].priorityNumber:  # checking the patrons based on priority and time of reserving
                    self.heap[index], self.heap[self.getRightChildIndex(index)] = self.heap[
                                                                                      self.getRightChildIndex(index)], \
                                                                                  self.heap[index]
                    index = self.getRightChildIndex(index)
                elif self.heap[index].priorityNumber > self.heap[self.getRightChildIndex(index)].priorityNumber > \
                        self.heap[self.getLeftChildIndex(index)].priorityNumber:  # checking based on priority number
                    self.heap[index], self.heap[self.getLeftChildIndex(index)] = self.heap[
                                                                                     self.getLeftChildIndex(index)], \
                                                                                 self.heap[index]
                    index = self.getLeftChildIndex(index)
                elif self.heap[index].timeOfReservation > self.heap[
                    self.getRightChildIndex(index)].timeOfReservation and self.heap[index].priorityNumber == self.heap[
                    self.getRightChildIndex(index)].priorityNumber < self.heap[
                    self.getLeftChildIndex(index)].priorityNumber:
                    self.heap[index], self.heap[self.getRightChildIndex(index)] = self.heap[
                                                                                      self.getRightChildIndex(index)], \
                                                                                  self.heap[index]
                    index = self.getRightChildIndex(index)
                elif self.heap[index].timeOfReservation > self.heap[self.getLeftChildIndex(index)].timeOfReservation and \
                        self.heap[index].priorityNumber == self.heap[self.getLeftChildIndex(index)].priorityNumber < \
                        self.heap[self.getRightChildIndex(index)].priorityNumber:
                    self.heap[index], self.heap[self.getLeftChildIndex(index)] = self.heap[
                                                                                     self.getLeftChildIndex(index)], \
                                                                                 self.heap[index]
                    index = self.getLeftChildIndex(index)
                elif self.heap[index].priorityNumber == self.heap[self.getLeftChildIndex(index)].priorityNumber == \
                        self.heap[self.getRightChildIndex(index)].priorityNumber:  # checking based on priority number
                    if self.heap[index].timeOfReservation > self.heap[
                        self.getRightChildIndex(index)].timeOfReservation < self.heap[
                        self.getLeftChildIndex(
                            index)].timeOfReservation:  # if there is a tie then we break it using the time of Reservation
                        self.heap[index], self.heap[self.getRightChildIndex(index)] = self.heap[self.getRightChildIndex(
                            index)], self.heap[index]
                        index = self.getRightChildIndex(index)
                    elif self.heap[index].timeOfReservation > self.heap[
                        self.getLeftChildIndex(index)].timeOfReservation < self.heap[
                        self.getRightChildIndex(index)].timeOfReservation:
                        self.heap[index], self.heap[self.getLeftChildIndex(index)] = self.heap[
                                                                                         self.getLeftChildIndex(index)], \
                                                                                     self.heap[index]
                        index = self.getLeftChildIndex(index)
                    else:
                        break
                else:
                    break
            elif self.hasLeftChild(index):
                if self.heap[index].priorityNumber > self.heap[self.getLeftChildIndex(index)].priorityNumber:
                    self.heap[index], self.heap[self.getLeftChildIndex(index)] = self.heap[
                                                                                     self.getLeftChildIndex(index)], \
                                                                                 self.heap[index]
                    index = self.getLeftChildIndex(index)
                elif (self.heap[index].priorityNumber == self.heap[self.getLeftChildIndex(index)].priorityNumber) and (
                        self.heap[index].timeOfReservation > self.heap[
                    self.getLeftChildIndex(index)].timeOfReservation):
                    self.heap[index], self.heap[self.getLeftChildIndex(index)] = self.heap[
                                                                                     self.getLeftChildIndex(index)], \
                                                                                 self.heap[index]
                    index = self.getLeftChildIndex(index)
                else:
                    break
            else:
                break
        return temp

    def printHeap(self):  # function to print the heap for debugging purpose
        for i in self.heap:
            print(i.patronID, end=" ")
        print()
