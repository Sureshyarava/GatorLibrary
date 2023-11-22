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
        if not self.hasParent(index):
            return -1
        return self.heap[index // 2]

    def getParentIndex(self, index):
        if not self.hasParent(index):
            return -1
        return index // 2

    def hasRightChild(self, index):
        return (2 * index + 2) < self.heapSize

    def getRightChild(self, index):
        if not self.hasRightChild(index):
            return -1
        return self.heap[(2 * index + 2)]

    def getRightChildIndex(self, index):
        if not self.hasRightChild(index):
            return -1
        return index * 2 + 2

    def hasLeftChild(self, index):
        return (2 * index + 1) < self.heapSize

    def getLeftChild(self, index):
        if not self.hasLeftChild(index):
            return -1
        return self.heap[(2 * index + 1)]

    def getLeftChildIndex(self, index):
        if not self.hasLeftChild(index):
            return -1
        return 2 * index + 1

    def push(self, patronID, priorityNumber):
        if self.heapSize >= 20:
            print("Wait list is Fill")
            return -1
        node = Node(patronID, priorityNumber)
        self.heapSize += 1
        self.heap.append(node)
        index = self.heapSize - 1
        while index != -1 and self.getParent(index) != -1:
            if (self.heap[index].priorityNumber < self.heap[self.getParentIndex(index)].priorityNumber) or (
                    self.heap[index].timeOfReservation < self.heap[self.getParentIndex(index)].timeOfReservation and
                    self.heap[index].priorityNumber == self.heap[self.getParentIndex(index)].priorityNumber):
                self.heap[self.getParentIndex(index)], self.heap[index] = self.heap[index], self.heap[
                    self.getParentIndex(index)]
                index = self.getParentIndex(index)
            else:
                break
        return 0

    def removeMin(self):
        if self.heapSize == 0:
            return -2
        elif self.heapSize == 1:
            temp = self.heap[0]
            self.heapSize -= 1
            self.heap = []
            return temp
        temp = self.heap[0]
        self.heap[0] = self.heap.pop(-1)
        self.heapSize -= 1
        index = 0
        while index != -1 and (self.getLeftChildIndex(index) != -1 or self.getRightChildIndex(index) != -1):
            if self.hasRightChild(index):
                if self.heap[index].priorityNumber > self.heap[self.getRightChildIndex(index)].priorityNumber and \
                        self.heap[self.getRightChildIndex(index)].priorityNumber < self.heap[
                    self.getLeftChildIndex(index)].priorityNumber:
                    self.heap[index], self.heap[self.getRightChildIndex(index)] = self.heap[
                                                                                      self.getRightChildIndex(index)], \
                                                                                  self.heap[index]
                    index = self.getRightChildIndex(index)
                elif self.heap[index].priorityNumber > self.heap[self.getRightChildIndex(index)].priorityNumber > \
                        self.heap[self.getLeftChildIndex(index)].priorityNumber:
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
                        self.heap[self.getRightChildIndex(index)].priorityNumber:
                    if self.heap[index].timeOfReservation > self.heap[
                        self.getRightChildIndex(index)].timeOfReservation < self.heap[
                        self.getLeftChildIndex(index)].timeOfReservation:
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

    def printHeap(self):
        for i in self.heap:
            print(i.patronID, end=" ")
        print()

# b = ReservationHeap(201,1)
# b.push(202,2)
# b.push(203,1)
# b.push(204,1)
# b.push(205,1)
# b.push(206,1)
# b.push(207,1)
# b.printHeap()
# k=b.removeMin()
# print("Minimum is removed ---------")
# print("Patron ID is {0} and priority Number is {1} and time of Reservation is {2}".format(k.patronID,
#                                                                                                        k.priorityNumber,
#                                                                                                        k.timeOfReservation))
# b.printHeap()
#
# b.removeMin()
# b.printHeap()
