import sys
import re

from RedBlackImplementation import RedBlackTree
from reservationHeap import ReservationHeap

redBlackTree = None  # Red black tree object reference

writeFileObject = None  # object reference for writing into a file


# Function to print information about a book node
def PrintBookNode(res):
    writeFileObject.write('BookID = {0}\n'.format(res.book.bookId))
    writeFileObject.write('Title = "{0}"\n'.format(res.book.bookName))
    writeFileObject.write('Author = "{0}"\n'.format(res.book.authorName))
    writeFileObject.write('Availability = "{0}"\n'.format(res.book.availabilityStatus))
    writeFileObject.write('BorrowedBy = {0}\n'.format(res.book.borrowedBy))
    res1 = []
    if res.book.reservationHeap:
        for i in res.book.reservationHeap.heap:
            res1.append(i.patronID)
        writeFileObject.write("Reservations = {0}\n".format(str(res1)))
    else:
        writeFileObject.write("Reservations = []\n")


# Function to print information about a specific book
def PrintBook(book_Id):
    res = redBlackTree.findNode(book_Id)
    if res:
        PrintBookNode(res)
    else:
        res = "Book {0} not found in the Library\n".format(book_Id)
        writeFileObject.write(res)


# Function to print information about books within a specified range
def PrintBooks(book_ID1, book_ID2):
    res = redBlackTree.getPreOrder(redBlackTree.head)
    for i in res:
        if book_ID1 <= i[0] <= book_ID2:
            PrintBookNode(i[1])
            writeFileObject.write("\n")


# Function to insert a new book into the library
def InsertBook(book_ID, bookName, authorName, availabilityStatus, borrowedBy=None, Heap=None):
    redBlackTree.insert(book_ID, bookName, authorName, availabilityStatus, borrowedBy, Heap)


# Function to handle book borrowing by a patron
def BorrowBook(patron_ID, book_ID, patron_Priority):
    node = redBlackTree.findNode(book_ID)
    if node.book.availabilityStatus == 'Yes':
        node.book.availabilityStatus = "No"
        node.book.borrowedBy = patron_ID
        writeFileObject.write("Book {0} Borrowed by Patron {1}\n".format(book_ID, patron_ID))
    else:
        if not node.book.reservationHeap:
            node.book.reservationHeap = ReservationHeap(patron_ID, patron_Priority)
        else:
            node.book.reservationHeap.push(patron_ID, patron_Priority)
        writeFileObject.write("Book {0} Reserved by Patron {1}\n".format(book_ID, patron_ID))


# Function to handle book return by a patron
def ReturnBook(patron_ID, book_ID):
    writeFileObject.write("Book {0} Returned by Patron {1}\n".format(book_ID, patron_ID))
    node = redBlackTree.findNode(book_ID)
    if node.book.reservationHeap:
        temp = node.book.reservationHeap
        tempPatron = temp.removeMin()
        if tempPatron != -2:
            node.book.borrowedBy = tempPatron.patronID
            writeFileObject.write("\n")
            writeFileObject.write("Book {0} Allotted to Patron {1}\n".format(book_ID, tempPatron.patronID))
    else:
        node.book.availabilityStatus = "Yes"
        node.book.borrowedBy = None


# Function to delete a book from the library
def DeleteBook(book_ID):
    node = redBlackTree.findNode(book_ID)
    if node.book.reservationHeap:
        string = ""
        for i in range(node.book.reservationHeap.heapSize):
            if i == node.book.reservationHeap.heapSize - 1:
                string += str(node.book.reservationHeap.heap[i].patronID)
            else:
                string += str(node.book.reservationHeap.heap[i].patronID) + ", "
        if node.book.reservationHeap.heapSize > 1:
            writeFileObject.write(
                "Book {0} is no longer available. Reservations made by Patrons {1} have been cancelled!\n".format(
                    book_ID,
                    string))
        else:
            writeFileObject.write(
                "Book {0} is no longer available. Reservations made by Patron {1} have been cancelled!\n".format(
                    book_ID,
                    string))
    else:
        writeFileObject.write("Book {0} is no longer available\n".format(book_ID))
    redBlackTree.deleteNode(node)


# Function to quit the program
def Quit():
    writeFileObject.write("Program Terminated!!\n")
    writeFileObject.close()
    sys.exit()


# Function to print the color flip count of the red-black tree
def ColorFlipCount():
    temp = redBlackTree.flipCount
    writeFileObject.write("Colour Flip Count: {0}\n".format(temp))


# Function to strip the line from the input File
def stripLine(String):
    strippedLine = str(String.strip())
    strippedLine = strippedLine[strippedLine.index("(") + 1:-1]
    return strippedLine.split(", ")


# Function to find the book closest to a specified target ID
def FindClosestBook(targetID):
    res = redBlackTree.getPreOrder(redBlackTree.head)
    result = []
    for i in res:
        result.append(abs(targetID - i[0]))
    minimum = min(result)
    for j in range(len(result)):
        if result[j] == minimum:
            PrintBookNode(res[j][1])
            writeFileObject.write("\n")


if __name__ == '__main__':
    # Read input file and initialize Red-Black tree
    inputFileName = sys.argv[1]
    redBlackTree = RedBlackTree()
    fileLocation = "./{0}".format(inputFileName)
    outPutFileLocation = "./{0}_output_file.txt".format(inputFileName.split(".")[0])
    outPutFile = open(outPutFileLocation, "w")
    writeFileObject = outPutFile
    inputFile = open(fileLocation, "r")
    Lines = inputFile.readlines()
    # Process each line in the input file
    for line in Lines:
        # Check the command type and perform the corresponding action
        inputParameters = stripLine(line)
        if "PrintBooks" in line:
            bookID1 = int(inputParameters[0])
            bookID2 = int(inputParameters[1])
            PrintBooks(bookID1, bookID2)
        elif "PrintBook" in line:
            bookId = int(inputParameters[0])
            PrintBook(bookId)
            writeFileObject.write("\n")
        elif "InsertBook" in line:
            pattern = r'InsertBook\((\d+), "(.*?)", "(.*?)", "(.*?)"\)'
            match = re.match(pattern, line)
            if match:
                book_id = int(match.group(1))
                title = match.group(2)
                author = match.group(3)
                availability = match.group(4)
                InsertBook(book_id, title, author, availability)
        elif "BorrowBook" in line:
            pattern = r'BorrowBook\((\d+), (\d+), (\d+)\)'
            match = re.match(pattern, line)
            if match:
                # Extracting values using group() method
                patronID = match.group(1)
                bookID = match.group(2)
                patronPriority = match.group(3)
                BorrowBook(int(patronID), int(bookID), int(patronPriority))
            writeFileObject.write("\n")
        elif "ReturnBook" in line:
            pattern = r'ReturnBook\((\d+), (\d+)\)'
            match = re.match(pattern, line)
            if match:
                patronID = match.group(1)
                bookID = match.group(2)
                ReturnBook(int(patronID), int(bookID))
            writeFileObject.write("\n")
        elif "Quit" in line:
            Quit()
            writeFileObject.write("\n")
        elif "ColorFlipCount" in line:
            ColorFlipCount()
            writeFileObject.write("\n")
        elif "DeleteBook" in line:
            bookId = int(inputParameters[0])
            DeleteBook(bookId)
            writeFileObject.write("\n")
        elif "FindClosestBook" in line:
            targetId = int(inputParameters[0])
            FindClosestBook(targetId)
            writeFileObject.write("\n")
