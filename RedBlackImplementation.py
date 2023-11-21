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
                parentOfGrandParent.leftChild.colour = False
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
    def findHighestBookFromLeftSubTree(node):
        temp = node.leftChild
        while temp.rightChild:
            temp = temp.rightChild
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
            highestBookOnLeftSubTree = RedBlackTree.findHighestBookFromLeftSubTree(node)
            parentOfHighestBookOnLeftSubTree = self.findParentOfChild(highestBookOnLeftSubTree)
            node.book = highestBookOnLeftSubTree.book
            degreeOfLeastNodeOnSubtree = 2 if (highestBookOnLeftSubTree.rightChild and highestBookOnLeftSubTree.leftChild) else 1
            degreeOfLeastNodeOnSubtree = 0 if not highestBookOnLeftSubTree.rightChild and not highestBookOnLeftSubTree.leftChild else degreeOfLeastNodeOnSubtree
            if not highestBookOnLeftSubTree.colour:
                self.deleteBlackNode(highestBookOnLeftSubTree, parentOfHighestBookOnLeftSubTree, degreeOfLeastNodeOnSubtree)
            else:
                self.deleteRedNode(highestBookOnLeftSubTree, parentOfHighestBookOnLeftSubTree, degreeOfLeastNodeOnSubtree)

    def deleteBlackNode(self, node, parentNode, degreeOfNode):
        if degreeOfNode == 0:
            if parentNode.leftChild == node:
                if (not parentNode.rightChild or not parentNode.rightChild.colour) and ((not parentNode.rightChild.leftChild and not parentNode.rightChild.rightChild) or ((parentNode.rightChild.leftChild and not parentNode.rightChild.leftChild.colour) and ( parentNode.rightChild.rightChild and not parentNode.rightChild.rightChild.colour))):
                    parentNode.leftChild = None
                    parentNode.rightChild.colour = True
                    if parentNode.colour:
                        parentNode.colour = False
                        RedBlackTree.flipCount += 1
                    else:
                        self.delete_fix(parentNode, self.findParentOfChild(parentNode))
                elif parentNode.rightChild and parentNode.rightChild.colour:
                    parentNode.colour = True
                    parentNode.rightChild.colour = False
                    RedBlackTree.flipCount += 2
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent is None:
                        temp = self.head.rightChild.leftChild
                        temp1 = self.head
                        self.head = temp1.rightChild
                        self.head.leftChild = temp1
                        temp1.rightChild = temp
                        temp1.leftChild = None
                        self.delete_fix(None, parentNode)
                    else:
                        if grandParent.leftChild == parentNode:
                            temp = parentNode.rightChild.leftChild
                            temp1 = parentNode
                            grandParent.leftChild = parentNode.rightChild
                            grandParent.leftChild.leftChild = temp1
                            temp1.rightChild = temp
                            temp1.leftChild = None
                            self.delete_fix(None, parentNode)
                        else:
                            temp = parentNode.rightChild.leftChild
                            temp1 = parentNode
                            grandParent.rightChild = parentNode.rightChild
                            grandParent.rightChild.leftChild = temp1
                            temp1.rightChild = temp
                            temp1.leftChild = None
                            self.delete_fix(None, parentNode)
                elif (parentNode.rightChild and not parentNode.rightChild.colour) and (parentNode.rightChild.leftChild and parentNode.rightChild.leftChild.colour) and (
                        not parentNode.rightChild.rightChild or (parentNode.rightChild.rightChild and not parentNode.rightChild.rightChild.colour)):
                    parentNode.rightChild.colour = True
                    parentNode.rightChild.leftChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentNode.rightChild
                    tempRight = parentNode.rightChild.leftChild.rightChild
                    parentNode.rightChild = parentNode.rightChild.leftChild
                    parentNode.rightChild.rightChild = temp
                    parentNode.rightChild.rightChild.leftChild = tempRight
                    self.deleteBlackNode(node, parentNode, degreeOfNode)
                elif (parentNode.rightChild and not parentNode.rightChild.colour) and (parentNode.rightChild.rightChild and parentNode.rightChild.rightChild.colour):
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent:
                        tempColour = parentNode.colour
                        temp1Colour = parentNode.rightChild.colour
                        if parentNode.rightChild.colour != tempColour:
                            parentNode.rightChild.colour = tempColour
                            parentNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        if grandParent.rightChild == parentNode:
                            tempParent = parentNode
                            temp = parentNode.rightChild.leftChild
                            grandParent.rightChild = parentNode.rightChild
                            grandParent.rightChild.leftChild = tempParent
                            tempParent.leftChild = None
                            tempParent.rightChild = temp
                            grandParent.rightChild.rightChild.colour = False
                            RedBlackTree.flipCount += 1
                        else:
                            tempParent = parentNode
                            temp = parentNode.rightChild.leftChild
                            grandParent.leftChild = parentNode.rightChild
                            grandParent.leftChild.leftChild = tempParent
                            tempParent.leftChild = None
                            tempParent.rightChild = temp
                            grandParent.leftChild.rightChild.colour = False
                            RedBlackTree.flipCount += 1
                    elif self.head == parentNode and not grandParent:
                        tempColour = parentNode.colour
                        temp1Colour = parentNode.rightChild.colour
                        if parentNode.rightChild.colour != tempColour:
                            parentNode.rightChild.colour = tempColour
                            parentNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        temp = self.head
                        self.head.leftChild = None
                        tempRight = self.head.rightChild.leftChild
                        self.head = self.head.rightChild
                        self.head.leftChild = temp
                        temp.rightChild = tempRight
                        self.head.rightChild.colour = False
                        RedBlackTree.flipCount += 1
            elif parentNode.rightChild == node:
                if (not parentNode.leftChild and not parentNode.leftChild.colour) and ((
                                                                                              not parentNode.leftChild.rightChild and not parentNode.leftChild.leftChild
                                                                                      ) or (
                        (parentNode.leftChild.leftChild and not parentNode.leftChild.leftChild.colour) and (parentNode.leftChild.rightChild and not parentNode.leftChild.rightChild.colour))):
                    parentNode.rightChild = None
                    parentNode.leftChild.colour = True
                    if parentNode.colour:
                        parentNode.colour = False
                        RedBlackTree.flipCount += 1
                    else:
                        self.delete_fix(parentNode, self.findParentOfChild(parentNode))
                elif parentNode.leftChild.colour:
                    parentNode.colour = True
                    parentNode.leftChild.colour = False
                    RedBlackTree.flipCount += 2
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent is None:
                        temp = self.head.leftChild.rightChild
                        temp1 = self.head
                        self.head = temp1.leftChild
                        self.head.rightChild = temp1
                        temp1.leftChild = temp
                        temp1.rightChild = None
                        self.delete_fix(None, parentNode)
                    else:
                        if grandParent.leftChild == parentNode:
                            temp = parentNode.leftChild.rightChild
                            temp1 = parentNode
                            grandParent.leftChild = parentNode.leftChild
                            grandParent.leftChild.rightChild = temp1
                            temp1.leftChild = temp
                            temp1.rightChild = None
                            self.delete_fix(None, parentNode)
                        else:
                            temp = parentNode.leftChild.rightChild
                            temp1 = parentNode
                            grandParent.rightChild = parentNode.leftChild
                            grandParent.rightChild.rightChild = temp1
                            temp1.leftChild = temp
                            temp1.rightChild = None
                            self.delete_fix(None, parentNode)
                elif not parentNode.leftChild.colour and (parentNode.leftChild.rightChild and parentNode.leftChild.rightChild.colour) and (not parentNode.leftChild.leftChild or (parentNode.leftChild.leftChild and not parentNode.leftChild.leftChild.colour)):
                    parentNode.leftChild.colour = True
                    parentNode.leftChild.rightChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentNode.leftChild
                    tempLeft = parentNode.leftChild.rightChild.leftChild
                    parentNode.leftChild = parentNode.leftChild.rightChild
                    parentNode.leftChild.leftChild = temp
                    temp.rightChild = tempLeft
                    self.deleteNode(node)
                elif not parentNode.leftChild.colour and (parentNode.leftChild.leftChild and parentNode.leftChild.leftChild.colour):
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent:
                        tempColour = parentNode.colour
                        temp1Colour = parentNode.leftChild.colour
                        if temp1Colour != tempColour:
                            parentNode.leftChild.colour = tempColour
                            parentNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        if grandParent.rightChild == parentNode:
                            tempParent = parentNode
                            temp = parentNode.leftChild.rightChild
                            grandParent.rightChild = parentNode.leftChild
                            grandParent.rightChild.rightChild = tempParent
                            tempParent.rightChild = None
                            tempParent.leftChild = temp
                            grandParent.rightChild.leftChild.colour = False
                            RedBlackTree.flipCount += 1
                        else:
                            tempParent = parentNode
                            temp = parentNode.leftChild.rightChild
                            grandParent.leftChild = parentNode.leftChild
                            grandParent.leftChild.rightChild = tempParent
                            tempParent.rightChild = None
                            tempParent.leftChild = temp
                            grandParent.leftChild.leftChild.colour = False
                            RedBlackTree.flipCount += 1
                    elif self.head == parentNode and not grandParent:
                        tempColour = parentNode.colour
                        temp1Colour = parentNode.leftChild.colour
                        if temp1Colour != tempColour:
                            parentNode.leftChild.colour = tempColour
                            parentNode.colour = tempColour
                            RedBlackTree.flipCount += 2
                        temp = self.head
                        self.head.rightChild = None
                        tempLeft = self.head.leftChild.rightChild
                        self.head = self.head.leftChild
                        self.head.rightChild = temp
                        temp.leftChild = tempLeft
                        self.head.leftChild.colour = False
                        RedBlackTree.flipCount += 1
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
                    parentNode.rightChild.colour = False
                    RedBlackTree.flipCount += 1
                elif node.leftChild:
                    pass  # This case won't arise
                elif node.rightChild and node.rightChild.colour:
                    parentNode.rightChild = node.rightChild
                    node.rightChild.colour = False
                    RedBlackTree.flipCount += 1
                elif node.rightChild:
                    pass  # This case won't arise
        else:
            highestNodeOnLeftSubtree = RedBlackTree.findHighestBookFromLeftSubTree(node)
            parentOfHighestBookOnLeftSubTree = self.findParentOfChild(highestNodeOnLeftSubtree)
            node.book = highestNodeOnLeftSubtree.book
            degreeOfLeastNodeOnSubtree = 2 if highestNodeOnLeftSubtree.rightChild and highestNodeOnLeftSubtree.leftChild else 1
            degreeOfLeastNodeOnSubtree = 0 if not highestNodeOnLeftSubtree.rightChild and not highestNodeOnLeftSubtree.leftChild else degreeOfLeastNodeOnSubtree
            if not highestNodeOnLeftSubtree.colour:
                self.deleteBlackNode(highestNodeOnLeftSubtree, parentOfHighestBookOnLeftSubTree,
                                     degreeOfLeastNodeOnSubtree)
            else:
                self.deleteRedNode(highestNodeOnLeftSubtree, parentOfHighestBookOnLeftSubTree, degreeOfLeastNodeOnSubtree)

    def delete_fix(self, node, parentOfNode):
        if self.head == node:
            return
        else:
            if parentOfNode.rightChild == node:
                if (not parentOfNode.leftChild or not parentOfNode.leftChild.colour) and ((
                                                                                              not parentOfNode.leftChild.rightChild and not parentOfNode.leftChild.leftChild
                                                                                      ) or (
                        (parentOfNode.leftChild.leftChild and not parentOfNode.leftChild.leftChild.colour) and (parentOfNode.leftChild.rightChild and not parentOfNode.leftChild.rightChild.colour))):
                    parentOfNode.leftChild.colour = True
                    if parentOfNode.colour:
                        parentOfNode.colour = False
                        RedBlackTree.flipCount += 1
                    else:
                        self.delete_fix(parentOfNode, self.findParentOfChild(parentOfNode))
                elif parentOfNode.leftChild.colour:
                    parentOfNode.colour = True
                    parentOfNode.leftChild.colour = False
                    RedBlackTree.flipCount += 2
                    grandParent = self.findParentOfChild(parentOfNode)
                    if grandParent is None:
                        temp = self.head.leftChild.rightChild
                        temp1 = self.head
                        self.head = temp1.leftChild
                        self.head.rightChild = temp1
                        temp1.leftChild = temp
                        temp1.rightChild = node
                        self.delete_fix(node, parentOfNode)
                    else:
                        if grandParent.leftChild == parentOfNode:
                            temp = parentOfNode.leftChild.rightChild
                            temp1 = parentOfNode
                            grandParent.leftChild = parentOfNode.leftChild
                            grandParent.leftChild.rightChild = temp1
                            temp1.leftChild = temp
                            temp1.rightChild = node
                            self.delete_fix(node, parentOfNode)
                        else:
                            temp = parentOfNode.leftChild.rightChild
                            temp1 = parentOfNode
                            grandParent.rightChild = parentOfNode.leftChild
                            grandParent.rightChild.rightChild = temp1
                            temp1.leftChild = temp
                            temp1.rightChild = node
                            self.delete_fix(node, parentOfNode)
                elif not parentOfNode.leftChild.colour and parentOfNode.leftChild.rightChild.colour and (not parentOfNode.leftChild.leftChild or (parentOfNode.leftChild.leftChild and not parentOfNode.leftChild.leftChild.colour)):
                    parentOfNode.leftChild.colour = True
                    parentOfNode.leftChild.rightChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentOfNode.leftChild
                    tempLeft = parentOfNode.leftChild.rightChild.leftChild
                    parentOfNode.leftChild = parentOfNode.leftChild.rightChild
                    parentOfNode.leftChild.leftChild = temp
                    temp.rightChild = tempLeft
                    self.delete_fix(node, parentOfNode)
                elif not parentOfNode.leftChild.colour and (parentOfNode.leftChild.leftChild and parentOfNode.leftChild.leftChild.colour):
                    grandParent = self.findParentOfChild(parentOfNode)
                    if grandParent:
                        tempColour = parentOfNode.colour
                        temp1Colour = parentOfNode.leftChild.colour
                        if temp1Colour != tempColour:
                            parentOfNode.leftChild.colour = tempColour
                            parentOfNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        if grandParent.rightChild == parentOfNode:
                            tempParent = parentOfNode
                            temp = parentOfNode.leftChild.rightChild
                            grandParent.rightChild = parentOfNode.leftChild
                            grandParent.rightChild.rightChild = tempParent
                            tempParent.rightChild = node
                            tempParent.leftChild = temp
                            grandParent.rightChild.leftChild.colour = False
                            RedBlackTree.flipCount += 1
                        else:
                            tempParent = parentOfNode
                            temp = parentOfNode.leftChild.rightChild
                            grandParent.leftChild = parentOfNode.leftChild
                            grandParent.leftChild.rightChild = tempParent
                            tempParent.rightChild = node
                            tempParent.leftChild = temp
                            grandParent.leftChild.leftChild.colour = False
                            RedBlackTree.flipCount += 1
                    elif self.head == parentOfNode and not grandParent:
                        tempColour = parentOfNode.colour
                        temp1Colour = parentOfNode.leftChild.colour
                        if temp1Colour != tempColour:
                            parentOfNode.leftChild.colour = tempColour
                            parentOfNode.colour = tempColour
                            RedBlackTree.flipCount += 2
                        temp = self.head
                        self.head.rightChild = node
                        tempLeft = self.head.leftChild.rightChild
                        self.head = self.head.leftChild
                        self.head.rightChild = temp
                        temp.leftChild = tempLeft
                        self.head.leftChild.colour = False
                        RedBlackTree.flipCount += 1
            elif parentOfNode.leftChild == node:
                if (not parentOfNode.rightChild or not parentOfNode.rightChild.colour) and ((
                                                                                                not parentOfNode.rightChild.leftChild and not parentOfNode.rightChild.rightChild) or (
                        (parentOfNode.rightChild.leftChild and not parentOfNode.rightChild.leftChild.colour) and (parentOfNode.rightChild.rightChild and not parentOfNode.rightChild.rightChild.colour))):
                    parentOfNode.rightChild.colour = True
                    if parentOfNode.colour:
                        parentOfNode.colour = False
                        RedBlackTree.flipCount += 1
                    else:
                        self.delete_fix(parentOfNode, self.findParentOfChild(parentOfNode))
                elif parentOfNode.rightChild.colour:
                    parentOfNode.colour = True
                    parentOfNode.rightChild.colour = False
                    RedBlackTree.flipCount += 2
                    grandParent = self.findParentOfChild(parentOfNode)
                    if grandParent is None:
                        temp = self.head.rightChild.leftChild
                        temp1 = self.head
                        self.head = temp1.rightChild
                        self.head.leftChild = temp1
                        temp1.rightChild = temp
                        temp1.leftChild = node
                        self.delete_fix(node, parentOfNode)
                    else:
                        if grandParent.leftChild == parentOfNode:
                            temp = parentOfNode.rightChild.leftChild
                            temp1 = parentOfNode
                            grandParent.leftChild = parentOfNode.rightChild
                            grandParent.leftChild.leftChild = temp1
                            temp1.rightChild = temp
                            temp1.leftChild = node
                            self.delete_fix(node, parentOfNode)
                        else:
                            temp = parentOfNode.rightChild.leftChild
                            temp1 = parentOfNode
                            grandParent.rightChild = parentOfNode.rightChild
                            grandParent.rightChild.leftChild = temp1
                            temp1.rightChild = temp
                            temp1.leftChild = node
                            self.delete_fix(node, parentOfNode)
                elif not parentOfNode.rightChild.colour and (parentOfNode.rightChild.leftChild and parentOfNode.rightChild.leftChild.colour) and (
                        not parentOfNode.rightChild.rightChild or (parentOfNode.rightChild.rightChild and not parentOfNode.rightChild.rightChild.colour)):
                    parentOfNode.rightChild.colour = True
                    parentOfNode.rightChild.leftChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentOfNode.rightChild
                    tempRight = parentOfNode.rightChild.leftChild.rightChild
                    parentOfNode.rightChild = parentOfNode.rightChild.leftChild
                    parentOfNode.rightChild.rightChild = temp
                    temp.leftChild = tempRight
                    self.delete_fix(node, parentOfNode)
                elif not parentOfNode.rightChild.colour and (parentOfNode.rightChild.rightChild and parentOfNode.rightChild.rightChild.colour):
                    grandParent = self.findParentOfChild(parentOfNode)
                    if grandParent:
                        tempColour = parentOfNode.colour
                        temp1Colour = parentOfNode.rightChild.colour
                        if parentOfNode.rightChild.colour != tempColour:
                            parentOfNode.rightChild.colour = tempColour
                            parentOfNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        if grandParent.rightChild == parentOfNode:
                            tempParent = parentOfNode
                            temp = parentOfNode.rightChild.leftChild
                            grandParent.rightChild = parentOfNode.rightChild
                            grandParent.rightChild.leftChild = tempParent
                            tempParent.leftChild = node
                            tempParent.rightChild = temp
                            grandParent.rightChild.rightChild.colour = False
                            RedBlackTree.flipCount += 1
                        else:
                            tempParent = parentOfNode
                            temp = parentOfNode.rightChild.leftChild
                            grandParent.leftChild = parentOfNode.rightChild
                            grandParent.leftChild.leftChild = tempParent
                            tempParent.leftChild = node
                            tempParent.rightChild = temp
                            grandParent.leftChild.rightChild.colour = False
                            RedBlackTree.flipCount += 1
                    elif self.head == parentOfNode and not grandParent:
                        tempColour = parentOfNode.colour
                        temp1Colour = parentOfNode.rightChild.colour
                        if parentOfNode.rightChild.colour != tempColour:
                            parentOfNode.rightChild.colour = tempColour
                            parentOfNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        temp = self.head
                        self.head.leftChild = node
                        tempRight = self.head.rightChild.leftChild
                        self.head = self.head.rightChild
                        self.head.leftChild = temp
                        temp.rightChild = tempRight
                        self.head.rightChild.colour = False
                        RedBlackTree.flipCount += 1

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

    def levelOrder(self, node):
        i = 0
        res = dict()
        res[i] = [node]
        while res[i]:
            res[i+1] = []
            for j in res[i]:
                if j:
                    print("node is {0} and colour is {1}".format(j.book.bookId, j.colour))
                    res[i+1].append(j.leftChild)
                    res[i+1].append(j.rightChild)
                else:
                    print("node is {0} and colour is {1}".format(None, None))
            print("End of level {0}".format(i))
            i += 1

    def print(self):
        self.levelOrder(self.head)

