# Gator Library

GatorLibrary is a fictional library management system designed to efficiently manage books, patrons, and borrowing operations. The system utilizes a Red-Black tree data structure for book management and a Binary Min-heap for handling book reservations. Each book node in the Red-Black tree is equipped with various attributes, including a reservation heap for tracking patron reservations.

## System Operations

<ol>
  <li>
    PrintBook(bookID)
    Print information about a specific book identified by its unique bookID.



```bash
    
    Output:
      If the bookID exists in the library:    BookID = <bookID>
                                                Title = "<bookName>"
                                                Author = "<Author Name>"
                                                Availability = "<Yes | No>"
                                                BorrowedBy = <Patron Id | None>
                                                Reservations = [patron1_id, patron2_id, ...]
      If the bookID is not found:  Book <bookID> not found in the Library
      
```
  </li>
<li>
  PrintBooks(bookID1, bookID2) 
  Print information about all books with bookIDs in the range [bookID1, bookID2].

  
```bash
      Output: BookID = <Book1 ID>
              Title = "<Book1 Name>"
              Author = "<Author1 Name>"
              Availability = "<Yes | No>"
              BorrowedBy = <Patron Id | None>
              Reservations = [patron1_id, patron2_id, ...]

              BookID = <Book2 ID>
              Title = "<Book2 Name>"
              Author = "<Author2 Name>"
              Availability = "<Yes | No>"
              BorrowedBy = <Patron Id | None>
              Reservations = [patron1_id, patron2_id, ...]
```
</li>

  <li>
    InsertBook(bookID, bookName, authorName, availabilityStatus, borrowedBy, reservationHeap)
    Add a new book to the library. BookID should be unique, and availability indicates whether the book is available for borrowing.
  </li>
  
  <li>
    BorrowBook(patronID, bookID, patronPriority)
    Allow a patron to borrow a book that is available and update the book's status. If a book is currently unavailable, create a reservation node in the heap as per the     patron's priority.
  </li>
  
<li>
  ReturnBook(patronID, bookID)
  Allow a patron to return a borrowed book. Update the book's status and assign the book to the patron with the highest priority in the Reservation Heap if there's a reservation.
</li>

<li>
  DeleteBook(bookID)
  Delete the book from the library and notify the patrons in the reservation list that the book is no longer available to borrow.
</li>

<li>
  FindClosestBook(targetID)
  Find the book with an ID closest to the given ID, checking on both sides. Print all details about the book. In case of ties, print both books ordered by bookIDs.
</li>

<li>
  ColorFlipCount()
  Track and analyze the frequency of color flips in the Red-Black tree structure during tree operations, such as insertion, deletion, and rotations.
</li>
</ol>


For running this code in your repo make sure to install python (preferred Version 3.6+)
<br>
And then run the command 


```bash
python3 gatorLibrary.py <filename>
```

You can provide your input inside the file and replace the filename above with the file you have created.
