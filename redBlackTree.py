import reservationHeap
import random


class Book:
    def __init__(self, bookId, bookName, authorName, availabilityStatus, borrowedBy, heap):
        self.bookId = bookId
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = borrowedBy
        self.reservationHeap = heap


class Node:
    def __init__(self, bookId, bookName, authorName, availabilityStatus, borrowedBy=None, heap=None):
        self.book = Book(bookId, bookName, authorName, borrowedBy, availabilityStatus, heap)
        self.leftChild = None
        self.rightChild = None
        self.colour = True  # True here indicates Red Color


class RedBlackTree:
    flipCount = 0

    def __init__(self):
        self.head = None

    @staticmethod
    def uncleRed(grandParent, parent):
        grandParent.colour = True
        parent.colour = False
        if grandParent.leftChild == parent:
            grandParent.rightChild.colour = False
        else:
            grandParent.leftChild.colour = False
        RedBlackTree.flipCount += 3

    def findParentOfChild(self, node):
        if node == self.head:
            return None  # if the node is the head then we return None
        temp = self.head
        while temp:
            if temp.leftChild == node:
                return temp
            elif temp.rightChild == node:
                return temp
            elif node.book.bookId < temp.book.bookId:
                temp = temp.leftChild
            elif node.book.bookId > temp.book.bookId:
                temp = temp.rightChild
            else:
                return None  # if the node is not found then we return None

    def handleLLBCase(self, grandParent, parent):
        if self.head == grandParent:
            temp = parent.rightChild
            tempHead = self.head
            self.head = parent
            self.head.rightChild = tempHead
            self.head.rightChild.leftChild = temp
            self.head.colour = False
            self.head.rightChild.colour = True
            RedBlackTree.flipCount += 2
        else:
            parentOfGrandParent = self.findParentOfChild(grandParent)
            if parentOfGrandParent.leftChild == grandParent:
                temp = parent.rightChild
                parentOfGrandParent.leftChild = parent
                parent.rightChild = grandParent
                grandParent.leftChild = temp
                parentOfGrandParent.leftChild.color = False
                parentOfGrandParent.leftChild.rightChild.colour = True
                RedBlackTree.flipCount += 2
            else:
                temp = parent.rightChild
                parentOfGrandParent.rightChild = parent
                parent.rightChild = grandParent
                grandParent.leftChild = temp
                parentOfGrandParent.rightChild.colour = False
                parentOfGrandParent.rightChild.rightChild.colour = True
                RedBlackTree.flipCount += 2

    def handleRRBCase(self, grandParent, parent):
        if self.head == grandParent:
            temp = parent.leftChild
            tempHead = self.head
            self.head = parent
            self.head.leftChild = tempHead
            self.head.leftChild.rightChild = temp
            self.head.colour = False
            self.head.leftChild.colour = True
            RedBlackTree.flipCount += 2
        else:
            parentOfGrandParent = self.findParentOfChild(grandParent)
            if parentOfGrandParent.leftChild == grandParent:
                temp = parent.leftChild
                parentOfGrandParent.leftChild = parent
                parent.leftChild = grandParent
                grandParent.rightChild = temp
                parentOfGrandParent.leftChild.colour = False
                parentOfGrandParent.leftChild.leftChild.colour = True
                RedBlackTree.flipCount += 2
            else:
                temp = parent.leftChild
                parentOfGrandParent.rightChild = parent
                parent.leftChild = grandParent
                grandParent.rightChild = temp
                parentOfGrandParent.rightChild.colour = False
                parentOfGrandParent.rightChild.leftChild.colour = True
                RedBlackTree.flipCount += 2

    def uncleBlack(self, grandParent, parent, child):
        if grandParent.leftChild == parent:
            if parent.leftChild == child:
                self.handleLLBCase(grandParent, parent)
            else:
                temp = child.leftChild
                grandParent.leftChild = child
                grandParent.leftChild.leftChild = parent
                parent.rightChild = temp
                self.handleLLBCase(grandParent, child)
        else:
            if parent.rightChild == child:
                self.handleRRBCase(grandParent, parent)
            else:
                temp = child.rightChild
                grandParent.rightChild = child
                child.rightChild = parent
                parent.leftChild = temp
                self.handleRRBCase(grandParent, child)

    def stabilize(self, node):
        if node == self.head:
            if node.colour:
                RedBlackTree.flipCount += 1
                node.colour = False
            return
        temp = self.head
        while temp:
            if temp.book.bookId > node.book.bookId and temp.leftChild.book.bookId > node.book.bookId == temp.leftChild.leftChild.book.bookId:
                grandParent = temp
                parent = temp.leftChild
                child = temp.leftChild.leftChild
                if parent.colour and child.colour and not grandParent.rightChild:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and not grandParent.rightChild.colour:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and grandParent.rightChild.colour:
                    RedBlackTree.uncleRed(grandParent, parent)
                    return self.stabilize(grandParent)
                else:
                    return
            elif temp.book.bookId > node.book.bookId and temp.leftChild.book.bookId < node.book.bookId == temp.leftChild.rightChild.book.bookId:
                grandParent = temp
                parent = temp.leftChild
                child = temp.leftChild.rightChild
                if parent.colour and child.colour and not grandParent.rightChild:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and not grandParent.rightChild.colour:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and grandParent.rightChild.colour:
                    RedBlackTree.uncleRed(grandParent, parent)
                    return self.stabilize(grandParent)
                else:
                    return
            elif temp.book.bookId < node.book.bookId and temp.rightChild.book.bookId > node.book.bookId == temp.rightChild.leftChild.book.bookId:
                grandParent = temp
                parent = temp.rightChild
                child = temp.rightChild.leftChild
                if parent.colour and child.colour and not grandParent.leftChild:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and not grandParent.leftChild.colour:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and grandParent.leftChild.colour:
                    RedBlackTree.uncleRed(grandParent, parent)
                    return self.stabilize(grandParent)
                else:
                    return
            elif temp.book.bookId < node.book.bookId and temp.rightChild.book.bookId < node.book.bookId == temp.rightChild.rightChild.book.bookId:
                grandParent = temp
                parent = temp.rightChild
                child = temp.rightChild.rightChild
                if parent.colour and child.colour and not grandParent.leftChild:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and not grandParent.leftChild.colour:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and grandParent.leftChild.colour:
                    RedBlackTree.uncleRed(grandParent, parent)
                    return self.stabilize(grandParent)
                else:
                    return
            elif temp.book.bookId < node.book.bookId:
                temp = temp.rightChild
            elif temp.book.bookId > node.book.bookId:
                temp = temp.leftChild
            else:
                return

    def insert(self, bookId, bookName, authorName, availabilityStatus):
        node = Node(bookId, bookName, authorName, availabilityStatus)
        if not self.head:
            self.head = node
            RedBlackTree.flipCount += 1
            self.head.colour = False
        else:
            temp = self.head
            if not temp.leftChild and temp.book.bookId > node.book.bookId:
                temp.leftChild = node
            elif not temp.rightChild and temp.book.bookId < node.book.bookId:
                temp.rightChild = node
            else:
                while temp:
                    if node.book.bookId < temp.book.bookId and temp.leftChild:
                        temp = temp.leftChild
                    elif node.book.bookId > temp.book.bookId and temp.rightChild:
                        temp = temp.rightChild
                    elif node.book.bookId < temp.book.bookId and not temp.leftChild:
                        temp.leftChild = node
                        self.stabilize(temp.leftChild)
                        break
                    elif node.book.bookId > temp.book.bookId and not temp.rightChild:
                        temp.rightChild = node
                        self.stabilize(temp.rightChild)
                        break
                    else:
                        break

    def findNode(self, bookId):
        temp = self.head
        while temp:
            if temp.book.bookId == bookId:
                return temp
            elif temp.book.bookId < bookId:
                temp = temp.rightChild
            else:
                temp = temp.leftChild
        return None

    @staticmethod
    def findLeastBookFromRightSubTree(node):
        temp = node.rightChild
        while temp.leftChild:
            temp = temp.leftChild
        return temp

    def deleteRedNode(self, node, parentOfNode, degreeOfNode):
        if degreeOfNode == 0:  # if the give book node colour is red and is a leaf node
            if parentOfNode.leftChild == node:
                parentOfNode.leftChild = None
            else:
                parentOfNode.rightChild = None
        elif degreeOfNode == 1:
            if parentOfNode.leftChild == node:  # remove the left child and replace with the node's child
                if node.leftChild:
                    parentOfNode.leftChild = node.leftChild
                else:
                    parentOfNode.leftChild = node.rightChild
            else:
                if node.leftChild:
                    parentOfNode.rightChild = node.leftChild
                else:
                    parentOfNode.rightChild = node.rightChild
        else:
            leastBookOnRightSubTree = RedBlackTree.findLeastBookFromRightSubTree(node)
            if not leastBookOnRightSubTree.colour:
                parentOfLeastBookOnRightSubTree = self.findParentOfChild(leastBookOnRightSubTree)
                degreeOfLeastNodeOnSubtree = 2 if (
                            leastBookOnRightSubTree.rightChild and leastBookOnRightSubTree.leftChild) else 1
                degreeOfLeastNodeOnSubtree = 0 if not leastBookOnRightSubTree.rightChild and not leastBookOnRightSubTree.leftChild else degreeOfLeastNodeOnSubtree
                self.deleteBlackNode(leastBookOnRightSubTree, parentOfLeastBookOnRightSubTree,
                                     degreeOfLeastNodeOnSubtree)
                leastBookOnRightSubTree.colour = True
                RedBlackTree.flipCount += 1
            else:
                parentOfLeastBookOnRightSubTree = self.findParentOfChild(leastBookOnRightSubTree)
                degreeOfLeastNodeOnSubtree = 2 if leastBookOnRightSubTree.rightChild and leastBookOnRightSubTree.leftChild else 1
                degreeOfLeastNodeOnSubtree = 0 if not leastBookOnRightSubTree.rightChild and not leastBookOnRightSubTree.leftChild else degreeOfLeastNodeOnSubtree
                self.deleteRedNode(leastBookOnRightSubTree, parentOfLeastBookOnRightSubTree, degreeOfLeastNodeOnSubtree)
            tempRightChild = node.rightChild
            tempLeftChild = node.leftChild
            leastBookOnRightSubTree.rightChild = tempRightChild
            leastBookOnRightSubTree.leftChild = tempLeftChild

            if parentOfNode.leftChild == node:
                parentOfNode.leftChild = leastBookOnRightSubTree
            else:
                parentOfNode.rightChild = leastBookOnRightSubTree

    def deleteBlackNode(self, node, parentNode, degreeOfNode):
        if degreeOfNode == 0:
            if parentNode:
                grandParent = self.findParentOfChild(parentNode)
                if parentNode == self.head:
                    if parentNode.leftChild == node:
                        if not parentNode.rightChild.leftChild and not parentNode.rightChild.rightChild:
                            parentNode.leftChild = None
                            parentNode.rightChild.colour = True
                            RedBlackTree.flipCount += 1
                        elif parentNode.rightChild.leftChild and parentNode.rightChild.rightChild:
                            if not parentNode.rightChild.leftChild.colour and not parentNode.rightChild.rightChild.colour:
                                parentNode.leftChild = None
                                parentNode.rightChild.colour = True
                                RedBlackTree.flipCount += 1
                            elif parentNode.rightChild.leftChild.colour and parentNode.rightChild.rightChild.colour:
                                temp = self.head
                                parentNode.leftChild = None
                                tempLeft = parentNode.rightChild.leftChild
                                self.head = self.head.rightChild
                                self.head.leftChild = temp
                                temp.rightChild = tempLeft
                                self.head.rightChild.colour = False
                                RedBlackTree.flipCount += 1
                        else:
                            if parentNode.rightChild.leftChild and not parentNode.rightChild.rightChild:
                                temp = parentNode.rightChild
                                parentNode.leftChild = None
                                tempRight = parentNode.rightChild.leftChild.rightChild
                                parentNode.rightChild = parentNode.rightChild.leftChild
                                parentNode.rightChild.rightChild = temp
                                parentNode.rightChild.rightChild.leftChild = tempRight
                                temp = parentNode
                                self.head = parentNode.rightChild
                                tempLeft = parentNode.rightChild.leftChild
                                self.head.colour = False
                                RedBlackTree.flipCount += 1
                                self.head.leftChild = temp
                                self.head.leftChild.rightChild = tempLeft
                            else:
                                temp = parentNode.rightChild.leftChild
                                tempLeft = parentNode
                                parentNode.leftChild = None
                                self.head = parentNode.rightChild
                                self.head.leftChild = tempLeft
                                self.head.leftChild.rightChild = temp
                                self.head.rightChild.colour = False
                                RedBlackTree.flipCount += 1
                    else:
                        if not parentNode.leftChild.leftChild and not parentNode.leftChild.rightChild:
                            parentNode.rightChild = None
                            parentNode.leftChild.colour = True
                            RedBlackTree.flipCount += 1
                        elif parentNode.leftChild.leftChild and parentNode.leftChild.rightChild:
                            if not parentNode.leftChild.leftChild.colour and not parentNode.leftChild.rightChild.colour:
                                parentNode.RightChild = None
                                parentNode.leftChild.colour = True
                                RedBlackTree.flipCount += 1
                            elif parentNode.leftChild.leftChild.colour and parentNode.leftChild.rightChild.colour:
                                temp = self.head
                                parentNode.rightChild = None
                                tempRight = parentNode.leftChild.rightChild
                                self.head = self.head.leftChild
                                self.head.rightChild = temp
                                temp.leftChild = tempRight
                                self.head.leftChild.colour = False
                                RedBlackTree.flipCount += 1
                        else:
                            if parentNode.leftChild.leftChild and not parentNode.leftChild.rightChild:
                                temp = parentNode.leftChild
                                parentNode.rightChild = None
                                tempLeft = parentNode.leftChild.rightChild.leftChild
                                parentNode.leftChild = parentNode.leftChild.rightChild
                                parentNode.leftChild.leftChild = temp
                                parentNode.leftChild.leftChild.rightChild = tempLeft
                                temp = parentNode
                                self.head = parentNode.leftChild
                                tempRight = parentNode.leftChild.rightChild
                                self.head.colour = False
                                RedBlackTree.flipCount += 1
                                self.head.rightChild = temp
                                self.head.rightChild.leftChild = tempRight
                            else:
                                temp = parentNode.leftChild.rightChild
                                tempRight = parentNode
                                parentNode.rightChild = None
                                self.head = parentNode.leftChild
                                self.head.rightChild = tempRight
                                self.head.leftChild.rightChild = temp
                                self.head.leftChild.colour = False
                                RedBlackTree.flipCount += 1
                else:
                    pass  # yet to be implemented
            else:
                self.head = None
        elif degreeOfNode == 1:
            if parentNode.leftChild == node:
                if node.leftChild and node.leftChild.colour:
                    parentNode.leftChild = node.leftChild
                    node.leftChild.colour = False
                    RedBlackTree.flipCount += 1
                elif node.leftChild:
                    pass  # This case won't arise
                elif node.rightChild and node.rightChild.colour:
                    parentNode.leftChild = node.rightChild
                    node.rightChild.colour = False
                    RedBlackTree.flipCount += 1
                elif node.rightChild:
                    pass  # This case won't arise
            else:
                if node.leftChild and node.leftChild.colour:
                    parentNode.rightChild = node.leftChild
                elif node.leftChild:
                    pass  # This case won't arise
                elif node.rightChild and node.rightChild.colour:
                    parentNode.rightChild = node.rightChild
                    node.rightChild.colour = False
                    RedBlackTree.flipCount += 1
                elif node.rightChild:
                    pass  # This case won't arise
        else:
            leastNodeOnRightSubtree = RedBlackTree.findLeastBookFromRightSubTree(node)
            if not leastNodeOnRightSubtree.colour:
                parentOfLeastBookOnRightSubTree = self.findParentOfChild(leastNodeOnRightSubtree)
                degreeOfLeastNodeOnSubtree = 2 if leastNodeOnRightSubtree.rightChild and leastNodeOnRightSubtree.leftChild else 1
                degreeOfLeastNodeOnSubtree = 0 if not leastNodeOnRightSubtree.rightChild and not leastNodeOnRightSubtree.leftChild else degreeOfLeastNodeOnSubtree
                self.deleteBlackNode(leastNodeOnRightSubtree, parentOfLeastBookOnRightSubTree,
                                     degreeOfLeastNodeOnSubtree)
            else:
                parentOfLeastBookOnRightSubTree = self.findParentOfChild(leastNodeOnRightSubtree)
                degreeOfLeastNodeOnSubtree = 2 if leastNodeOnRightSubtree.rightChild and leastNodeOnRightSubtree.leftChild else 1
                degreeOfLeastNodeOnSubtree = 0 if not leastNodeOnRightSubtree.rightChild and not leastNodeOnRightSubtree.leftChild else degreeOfLeastNodeOnSubtree
                self.deleteRedNode(leastNodeOnRightSubtree, parentOfLeastBookOnRightSubTree, degreeOfLeastNodeOnSubtree)
                leastNodeOnRightSubtree.colour = False
                RedBlackTree.flipCount += 1
            tempRightChild = node.rightChild
            tempLeftChild = node.leftChild
            leastNodeOnRightSubtree.rightChild = tempRightChild
            leastNodeOnRightSubtree.leftChild = tempLeftChild
            if parentNode:
                if parentNode.leftChild == node:
                    parentNode.leftChild = leastNodeOnRightSubtree
                else:
                    parentNode.rightChild = leastNodeOnRightSubtree
            else:
                self.head = leastNodeOnRightSubtree

    def deleteNode(self, node):
        degreeOfNode = 2 if node.leftChild and node.rightChild else 1
        degreeOfNode = 0 if not node.leftChild and not node.rightChild else degreeOfNode
        if node == self.head and degreeOfNode == 0:
            self.head = None
            return
        parentOfNode = self.findParentOfChild(node)
        if node.colour:
            self.deleteRedNode(node, parentOfNode, degreeOfNode)
        else:
            self.deleteBlackNode(node, parentOfNode, degreeOfNode)

    def deleteBook(self, bookId):
        node = self.findNode(bookId)
        if node is None:
            print("Book is not present in the Library")
        else:
            self.deleteNode(node)

    def preOrder(self, node):
        if not node:
            return
        self.preOrder(node.leftChild)
        print("Node is {0} and node colour is {1}".format(node.book.bookId, node.colour))
        self.preOrder(node.rightChild)

    def print(self):
        self.preOrder(self.head)


rb = RedBlackTree()
rb.insert(23, '1', '1', '1')
rb.insert(7, '1', '1', '1')
rb.insert(59, '1', '1', '1')
rb.insert(56, '1', '1', '1')
# rb.insert(2, '1', '1', '1')
# rb.insert(35, '1', '1', '1')
# rb.insert(53, '1', '1', '1')
# rb.insert(3, '1', '1', '1')
# rb.insert(88, '1', '1', '1')
# rb.insert(26, '1', '1', '1')
# rb.insert(22, '1', '1', '1')
# rb.insert(92, '1', '1', '1')
# rb.insert(49, '1', '1', '1')
# rb.insert(98, '1', '1', '1')
# rb.insert(75, '1', '1', '1')
# rb.insert(58, '1', '1', '1')
# rb.insert(62, '1', '1', '1')
rb.print()
rb.deleteBook(7)
print("deleted node 7")
rb.print()
