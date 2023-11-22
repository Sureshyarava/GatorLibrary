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
        self.book = Book(bookId, bookName, authorName, availabilityStatus, borrowedBy, heap)
        self.leftChild = None
        self.rightChild = None
        self.colour = True  # True here indicates Red Color


class RedBlackTree:
    flipCount = 0

    def __init__(self, head=None):
        self.head = head

    # Condition when the uncle node is red then trying to flip the colour and balancing the red black tree
    @staticmethod
    def uncleRed(grandParent, parent):
        grandParent.colour = True
        parent.colour = False
        if grandParent.leftChild == parent:
            grandParent.rightChild.colour = False
        else:
            grandParent.leftChild.colour = False
        RedBlackTree.flipCount += 3

    def findParentOfChild(self, node):  # function to find the parent of the child provided with the node
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

    def handleLLBCase(self, grandParent, parent):  # function to handle LLb case in insertion
        if self.head == grandParent:  # if the given parent is self.head and there is no grandparent
            temp = parent.rightChild
            tempHead = self.head  # rotating the child with respect to the parent
            self.head = parent
            self.head.rightChild = tempHead
            self.head.rightChild.leftChild = temp
            self.head.colour = False
            self.head.rightChild.colour = True
            RedBlackTree.flipCount += 2
        else:
            parentOfGrandParent = self.findParentOfChild(grandParent)  # if there is grandparent then I am finding the grandParent and then rotating with respect to grand Parent
            if parentOfGrandParent.leftChild == grandParent:  # if the parent node is left of grandParent
                temp = parent.rightChild
                parentOfGrandParent.leftChild = parent
                parent.rightChild = grandParent
                grandParent.leftChild = temp
                parentOfGrandParent.leftChild.colour = False
                parentOfGrandParent.leftChild.rightChild.colour = True
                RedBlackTree.flipCount += 2
            else:    # if the parent node is right of grandParent
                temp = parent.rightChild
                parentOfGrandParent.rightChild = parent
                parent.rightChild = grandParent
                grandParent.leftChild = temp
                parentOfGrandParent.rightChild.colour = False
                parentOfGrandParent.rightChild.rightChild.colour = True
                RedBlackTree.flipCount += 2

    def handleRRBCase(self, grandParent, parent):  # function to handle RRb case while insertion
        if self.head == grandParent:  # if there is no grandParent then rotating with respect to self.head
            temp = parent.leftChild
            tempHead = self.head
            self.head = parent
            self.head.leftChild = tempHead
            self.head.leftChild.rightChild = temp
            self.head.colour = False
            self.head.leftChild.colour = True
            RedBlackTree.flipCount += 2
        else:
            parentOfGrandParent = self.findParentOfChild(grandParent)  # if there is grandparent then fetching the grandparent
            if parentOfGrandParent.leftChild == grandParent:  # if the parent node is left of grandparent then this condition satisfies
                temp = parent.leftChild
                parentOfGrandParent.leftChild = parent
                parent.leftChild = grandParent
                grandParent.rightChild = temp
                parentOfGrandParent.leftChild.colour = False
                parentOfGrandParent.leftChild.leftChild.colour = True
                RedBlackTree.flipCount += 2
            else:  # if the parent is right of Grandparent then this condition satisfies
                temp = parent.leftChild
                parentOfGrandParent.rightChild = parent
                parent.leftChild = grandParent
                grandParent.rightChild = temp
                parentOfGrandParent.rightChild.colour = False
                parentOfGrandParent.rightChild.leftChild.colour = True
                RedBlackTree.flipCount += 2

    def uncleBlack(self, grandParent, parent, child):  # handling four different cases in when uncle is black
        if grandParent.leftChild == parent:  # handling X = L case
            if parent.leftChild == child:
                self.handleLLBCase(grandParent, parent)
            else:   # handling LRb case
                temp = child.leftChild
                grandParent.leftChild = child
                grandParent.leftChild.leftChild = parent
                parent.rightChild = temp
                self.handleLLBCase(grandParent, child)
        else:  # handling  X = R case
            if parent.rightChild == child:
                self.handleRRBCase(grandParent, parent)
            else:  # handling RLb Case
                temp = child.rightChild
                grandParent.rightChild = child
                child.rightChild = parent
                parent.leftChild = temp
                self.handleRRBCase(grandParent, child)

    def stabilize(self, node):  # After insertions there may be some properties of Red black tree violating to handle those this function is used
        if node == self.head:
            # If the current node is the head of the tree and it is red,
            # flip its color to black and increment flip count.
            if node.colour:
                RedBlackTree.flipCount += 1
                node.colour = False
            return
        temp = self.head
        while temp:
            if temp.book.bookId > node.book.bookId and temp.leftChild.book.bookId > node.book.bookId == temp.leftChild.leftChild.book.bookId:
                # Left-Left case
                grandParent = temp
                parent = temp.leftChild
                child = temp.leftChild.leftChild
                # Check the color of parent, child, and grandparent to determine the case.
                if parent.colour and child.colour and not grandParent.rightChild:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and not grandParent.rightChild.colour:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and grandParent.rightChild.colour:
                    # If uncle is red, perform an uncle-red operation.
                    RedBlackTree.uncleRed(grandParent, parent)
                    return self.stabilize(grandParent)
                else:
                    # If no violation is found, return.
                    return
            elif temp.book.bookId > node.book.bookId and temp.leftChild.book.bookId < node.book.bookId == temp.leftChild.rightChild.book.bookId:
                grandParent = temp # Left-Right case
                parent = temp.leftChild
                child = temp.leftChild.rightChild
                # Check the color of parent, child, and grandparent to determine the case.
                if parent.colour and child.colour and not grandParent.rightChild:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and not grandParent.rightChild.colour:
                    return self.uncleBlack(grandParent, parent, child)
                elif parent.colour and child.colour and grandParent.rightChild.colour:
                    # If uncle is red, perform an uncle-red operation.
                    RedBlackTree.uncleRed(grandParent, parent)
                    return self.stabilize(grandParent)
                else:
                    # If no violation is found, return.
                    return
            elif temp.book.bookId < node.book.bookId and temp.rightChild.book.bookId > node.book.bookId == temp.rightChild.leftChild.book.bookId:
                grandParent = temp # Right-Left case
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
                grandParent = temp # Right-Right case
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

    #  function to insert book into the Red black tree
    def insert(self, bookId, bookName, authorName, availabilityStatus, borrowedBy=None, heap=None):
        node = Node(bookId, bookName, authorName, availabilityStatus, borrowedBy, heap)
        if not self.head:  # if the red black tree is empty then assigning the head with the present new node
            self.head = node
            RedBlackTree.flipCount += 1
            self.head.colour = False
        else:
            temp = self.head  # if already there is red black tree which is not empty then it goes thorough this
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

    def findNode(self, bookId):  # function to find the Node provided with the bookId
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
    def findHighestBookFromLeftSubTree(node):  # function to find the highest book from the left Subtree
        temp = node.leftChild
        while temp.rightChild:
            temp = temp.rightChild
        return temp

    def deleteRedNode(self, node, parentOfNode, degreeOfNode):  # function to handle the deletion cases for Red node
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
        else:  # if the node to be deleted has 2 children then trying to replace the node with the highest child from the left Sutree
            highestBookOnLeftSubTree = RedBlackTree.findHighestBookFromLeftSubTree(node)
            parentOfHighestBookOnLeftSubTree = self.findParentOfChild(highestBookOnLeftSubTree)
            node.book = highestBookOnLeftSubTree.book
            degreeOfLeastNodeOnSubtree = 2 if (
                    highestBookOnLeftSubTree.rightChild and highestBookOnLeftSubTree.leftChild) else 1
            degreeOfLeastNodeOnSubtree = 0 if not highestBookOnLeftSubTree.rightChild and not highestBookOnLeftSubTree.leftChild else degreeOfLeastNodeOnSubtree
            if not highestBookOnLeftSubTree.colour:
                self.deleteBlackNode(highestBookOnLeftSubTree, parentOfHighestBookOnLeftSubTree,
                                     degreeOfLeastNodeOnSubtree)
            else:
                self.deleteRedNode(highestBookOnLeftSubTree, parentOfHighestBookOnLeftSubTree,
                                   degreeOfLeastNodeOnSubtree)

    def deleteBlackNode(self, node, parentNode, degreeOfNode):  # function to handle Deletion of black node
        if degreeOfNode == 0:  # if the node has no children
            if parentNode.leftChild == node:  # checking if the leftChild is the node to be deleted
                if (not parentNode.rightChild or not parentNode.rightChild.colour) and (
                        (not parentNode.rightChild.leftChild and not parentNode.rightChild.rightChild) or (
                        (parentNode.rightChild.leftChild and not parentNode.rightChild.leftChild.colour) and (
                        parentNode.rightChild.rightChild and not parentNode.rightChild.rightChild.colour))):  # checking sibling and sibling siblings colour and handling the cases
                    parentNode.leftChild = None
                    parentNode.rightChild.colour = True
                    if parentNode.colour:
                        parentNode.colour = False
                        RedBlackTree.flipCount += 1
                    else:
                        self.delete_fix(parentNode, self.findParentOfChild(parentNode))
                elif parentNode.rightChild and parentNode.rightChild.colour:   # checking if right Child is present and it's colour is red
                    parentNode.colour = True
                    parentNode.rightChild.colour = False
                    RedBlackTree.flipCount += 2
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent is None:  # if there is no grand Parent
                        temp = self.head.rightChild.leftChild
                        temp1 = self.head
                        self.head = temp1.rightChild
                        self.head.leftChild = temp1
                        temp1.rightChild = temp
                        temp1.leftChild = None
                        self.delete_fix(None, parentNode)
                    else:  # if there is grandParent
                        if grandParent.leftChild == parentNode:  # if the parent is left of grand Parent
                            temp = parentNode.rightChild.leftChild
                            temp1 = parentNode
                            grandParent.leftChild = parentNode.rightChild
                            grandParent.leftChild.leftChild = temp1
                            temp1.rightChild = temp
                            temp1.leftChild = None
                            self.delete_fix(None, parentNode)
                        else:  # if the parent is right of grand Parent
                            temp = parentNode.rightChild.leftChild
                            temp1 = parentNode
                            grandParent.rightChild = parentNode.rightChild
                            grandParent.rightChild.leftChild = temp1
                            temp1.rightChild = temp
                            temp1.leftChild = None
                            self.delete_fix(None, parentNode)
                elif (parentNode.rightChild and not parentNode.rightChild.colour) and (
                        parentNode.rightChild.leftChild and parentNode.rightChild.leftChild.colour) and (
                        not parentNode.rightChild.rightChild or (
                        parentNode.rightChild.rightChild and not parentNode.rightChild.rightChild.colour)):  # handling the vice versa cases of the above
                    parentNode.rightChild.colour = True
                    parentNode.rightChild.leftChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentNode.rightChild
                    tempRight = parentNode.rightChild.leftChild.rightChild
                    parentNode.rightChild = parentNode.rightChild.leftChild
                    parentNode.rightChild.rightChild = temp
                    parentNode.rightChild.rightChild.leftChild = tempRight
                    self.deleteBlackNode(node, parentNode, degreeOfNode)
                elif (parentNode.rightChild and not parentNode.rightChild.colour) and (
                        parentNode.rightChild.rightChild and parentNode.rightChild.rightChild.colour):  # checking sibling and sibling siblings colour
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent:  # if there is grandparent rotating with respect to grandParent
                        tempColour = parentNode.colour
                        temp1Colour = parentNode.rightChild.colour
                        if parentNode.rightChild.colour != tempColour:
                            parentNode.rightChild.colour = tempColour
                            parentNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        if grandParent.rightChild == parentNode:  # checking if the node is right of GrandParent
                            tempParent = parentNode
                            temp = parentNode.rightChild.leftChild
                            grandParent.rightChild = parentNode.rightChild
                            grandParent.rightChild.leftChild = tempParent
                            tempParent.leftChild = None
                            tempParent.rightChild = temp
                            grandParent.rightChild.rightChild.colour = False
                            RedBlackTree.flipCount += 1
                        else:   # checking if the node is left of grandparent
                            tempParent = parentNode
                            temp = parentNode.rightChild.leftChild
                            grandParent.leftChild = parentNode.rightChild
                            grandParent.leftChild.leftChild = tempParent
                            tempParent.leftChild = None
                            tempParent.rightChild = temp
                            grandParent.leftChild.rightChild.colour = False
                            RedBlackTree.flipCount += 1
                    elif self.head == parentNode and not grandParent: # checking if there is no grandparent and rotating with respect to head
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
            elif parentNode.rightChild == node:  # handling the vice versa cases of the above
                if (not parentNode.leftChild and not parentNode.leftChild.colour) and ((
                                                                                               not parentNode.leftChild.rightChild and not parentNode.leftChild.leftChild
                                                                                       ) or (
                                                                                               (
                                                                                                       parentNode.leftChild.leftChild and not parentNode.leftChild.leftChild.colour) and (
                                                                                                       parentNode.leftChild.rightChild and not parentNode.leftChild.rightChild.colour))):
                    parentNode.rightChild = None
                    parentNode.leftChild.colour = True
                    if parentNode.colour:
                        parentNode.colour = False
                        RedBlackTree.flipCount += 1
                    else:
                        self.delete_fix(parentNode, self.findParentOfChild(parentNode))
                elif parentNode.leftChild.colour:  # checking if it is the left Child
                    parentNode.colour = True
                    parentNode.leftChild.colour = False
                    RedBlackTree.flipCount += 2
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent is None:  # checking if this has no grandParent
                        temp = self.head.leftChild.rightChild
                        temp1 = self.head
                        self.head = temp1.leftChild
                        self.head.rightChild = temp1
                        temp1.leftChild = temp
                        temp1.rightChild = None
                        self.delete_fix(None, parentNode)
                    else:  # checking if this has grandparent
                        if grandParent.leftChild == parentNode: # checking if parent is left of grandParent
                            temp = parentNode.leftChild.rightChild
                            temp1 = parentNode
                            grandParent.leftChild = parentNode.leftChild
                            grandParent.leftChild.rightChild = temp1
                            temp1.leftChild = temp
                            temp1.rightChild = None
                            self.delete_fix(None, parentNode)
                        else:  # checking if parent is right of grandParent
                            temp = parentNode.leftChild.rightChild
                            temp1 = parentNode
                            grandParent.rightChild = parentNode.leftChild
                            grandParent.rightChild.rightChild = temp1
                            temp1.leftChild = temp
                            temp1.rightChild = None
                            self.delete_fix(None, parentNode)
                elif not parentNode.leftChild.colour and (
                        parentNode.leftChild.rightChild and parentNode.leftChild.rightChild.colour) and (
                        not parentNode.leftChild.leftChild or (
                        parentNode.leftChild.leftChild and not parentNode.leftChild.leftChild.colour)):  # checking sibling and sibling sibling's colour
                    parentNode.leftChild.colour = True
                    parentNode.leftChild.rightChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentNode.leftChild
                    tempLeft = parentNode.leftChild.rightChild.leftChild
                    parentNode.leftChild = parentNode.leftChild.rightChild
                    parentNode.leftChild.leftChild = temp
                    temp.rightChild = tempLeft
                    self.deleteNode(node)
                elif not parentNode.leftChild.colour and (
                        parentNode.leftChild.leftChild and parentNode.leftChild.leftChild.colour):
                    grandParent = self.findParentOfChild(parentNode)
                    if grandParent:  #  fetching the grandParent
                        tempColour = parentNode.colour
                        temp1Colour = parentNode.leftChild.colour
                        if temp1Colour != tempColour:  # If the colour of parent and children are different
                            parentNode.leftChild.colour = tempColour
                            parentNode.colour = temp1Colour
                            RedBlackTree.flipCount += 2
                        if grandParent.rightChild == parentNode:  # if the parent is right of grandparent
                            tempParent = parentNode
                            temp = parentNode.leftChild.rightChild
                            grandParent.rightChild = parentNode.leftChild
                            grandParent.rightChild.rightChild = tempParent
                            tempParent.rightChild = None
                            tempParent.leftChild = temp
                            grandParent.rightChild.leftChild.colour = False
                            RedBlackTree.flipCount += 1
                        else:  # if the parent is left of grandParent
                            tempParent = parentNode
                            temp = parentNode.leftChild.rightChild
                            grandParent.leftChild = parentNode.leftChild
                            grandParent.leftChild.rightChild = tempParent
                            tempParent.rightChild = None
                            tempParent.leftChild = temp
                            grandParent.leftChild.leftChild.colour = False
                            RedBlackTree.flipCount += 1
                    elif self.head == parentNode and not grandParent: # if there is no grandparent
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
        elif degreeOfNode == 1:  # if the node to be deleted has 1 child
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
        else: # if the node to be deleted has 2 children
            highestNodeOnLeftSubtree = RedBlackTree.findHighestBookFromLeftSubTree(node)
            parentOfHighestBookOnLeftSubTree = self.findParentOfChild(highestNodeOnLeftSubtree)
            node.book = highestNodeOnLeftSubtree.book
            degreeOfLeastNodeOnSubtree = 2 if highestNodeOnLeftSubtree.rightChild and highestNodeOnLeftSubtree.leftChild else 1
            degreeOfLeastNodeOnSubtree = 0 if not highestNodeOnLeftSubtree.rightChild and not highestNodeOnLeftSubtree.leftChild else degreeOfLeastNodeOnSubtree
            if not highestNodeOnLeftSubtree.colour:
                self.deleteBlackNode(highestNodeOnLeftSubtree, parentOfHighestBookOnLeftSubTree,
                                     degreeOfLeastNodeOnSubtree)
            else:
                self.deleteRedNode(highestNodeOnLeftSubtree, parentOfHighestBookOnLeftSubTree,
                                   degreeOfLeastNodeOnSubtree)

    def delete_fix(self, node, parentOfNode):  # function to help the delete function above to fix the balancing
        if self.head == node:
            return
        else:
            if parentOfNode.rightChild == node:
                if (not parentOfNode.leftChild or not parentOfNode.leftChild.colour) and ((
                                                                                                  not parentOfNode.leftChild.rightChild and not parentOfNode.leftChild.leftChild
                                                                                          ) or (
                                                                                                  (
                                                                                                          parentOfNode.leftChild.leftChild and not parentOfNode.leftChild.leftChild.colour) and (
                                                                                                          parentOfNode.leftChild.rightChild and not parentOfNode.leftChild.rightChild.colour))):
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
                elif not parentOfNode.leftChild.colour and parentOfNode.leftChild.rightChild.colour and (
                        not parentOfNode.leftChild.leftChild or (
                        parentOfNode.leftChild.leftChild and not parentOfNode.leftChild.leftChild.colour)):
                    parentOfNode.leftChild.colour = True
                    parentOfNode.leftChild.rightChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentOfNode.leftChild
                    tempLeft = parentOfNode.leftChild.rightChild.leftChild
                    parentOfNode.leftChild = parentOfNode.leftChild.rightChild
                    parentOfNode.leftChild.leftChild = temp
                    temp.rightChild = tempLeft
                    self.delete_fix(node, parentOfNode)
                elif not parentOfNode.leftChild.colour and (
                        parentOfNode.leftChild.leftChild and parentOfNode.leftChild.leftChild.colour):
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
                                                                                                    (
                                                                                                            parentOfNode.rightChild.leftChild and not parentOfNode.rightChild.leftChild.colour) and (
                                                                                                            parentOfNode.rightChild.rightChild and not parentOfNode.rightChild.rightChild.colour))):
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
                elif not parentOfNode.rightChild.colour and (
                        parentOfNode.rightChild.leftChild and parentOfNode.rightChild.leftChild.colour) and (
                        not parentOfNode.rightChild.rightChild or (
                        parentOfNode.rightChild.rightChild and not parentOfNode.rightChild.rightChild.colour)):
                    parentOfNode.rightChild.colour = True
                    parentOfNode.rightChild.leftChild.colour = False
                    RedBlackTree.flipCount += 2
                    temp = parentOfNode.rightChild
                    tempRight = parentOfNode.rightChild.leftChild.rightChild
                    parentOfNode.rightChild = parentOfNode.rightChild.leftChild
                    parentOfNode.rightChild.rightChild = temp
                    temp.leftChild = tempRight
                    self.delete_fix(node, parentOfNode)
                elif not parentOfNode.rightChild.colour and (
                        parentOfNode.rightChild.rightChild and parentOfNode.rightChild.rightChild.colour):
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

    def deleteNode(self, node):  # function to delete the Node
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

    def deleteBook(self, bookId):  # function to delete the book
        node = self.findNode(bookId)
        if node is None:
            print("Book is not present in the Library")
        else:
            self.deleteNode(node)

    def levelOrder(self, node):  # function to print the tree in level order for debugging purpose
        i = 0
        res = dict()
        res[i] = [node]
        while res[i]:
            res[i + 1] = []
            for j in res[i]:
                if j:
                    print("node is {0} and colour is {1}".format(j.book.bookId, j.colour))
                    res[i + 1].append(j.leftChild)
                    res[i + 1].append(j.rightChild)
                else:
                    print("node is {0} and colour is {1}".format(None, None))
            print("End of level {0}".format(i))
            i += 1

    def print(self):  # function to initiate level order traversal
        self.levelOrder(self.head)

    def getPreOrder(self, node):  # function to get the preorder traversal of the redblack tree
        res = []

        def preOrder(node):
            if not node:  # if node is none then break
                return
            preOrder(node.leftChild)
            res.append((node.book.bookId, node))
            preOrder(node.rightChild)
        preOrder(node)
        return res
