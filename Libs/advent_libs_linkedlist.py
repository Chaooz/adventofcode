
import sys
from advent_libs import *

class LinkedElement:
    GlobalID:int = 0
    elementId: int

    def __init__(self):
        self.elementId = LinkedElement.GlobalID
        self.prev = None
        self.next = None
        LinkedElement.GlobalID = LinkedElement.GlobalID + 1

    def ToString(self):
        extra = ""
        if self.prev is not None:
            extra = extra + " Prev:" + str(self.prev.elementId)
        if self.next is not None:
            extra = extra + " Next:" + str(self.next.elementId)
        return "[ID:" + str(self.elementId) + extra + "]"

    def GetNext(self):
        print_assert(self.next != self, "LinkedElement.GetNext() looped to itself")
        return self.next

    def FixLinks(self):
        if self.prev is not None:
            self.prev.next = self
        if self.next is not None:
            self.next.prev = self

        if self.next is not None:
            print_assert(self.next != self, "LinkedElement.FixLinks() looped to itself")
        if self.prev is not None:
            print_assert(self.prev != self, "LinkedElement.FixLinks() looped to itself")
        if self.next is not None and self.next == self.prev:
            print_assert(False, "LinkedElement.FixLinks() next == prev")

class LinkedList:

    firstElement:LinkedElement
    lastElement:LinkedElement
    numElements:int

    def __init__(self):
        self.firstElement = None
        self.lastElement = None
        self.numElements = 0

    def ToString(self, title:str = "", maxElements:int = -1):
        p = "\n"
        element = self.firstElement
        i = 0
        elements = 0
        print("LinkedList.ToString(" + title + ")")
        while element is not None:
            elements = elements + 1
            if maxElements > 0 and elements > maxElements:
                break

            p += element.ToString() + "\n"
            if element.next == element:
                print(p)
                print_assert(False, "LinkedList.ToString(" + title + ") looped to itself")
            element = element.GetNext() 
            i += 1
            if i> self.numElements:
                print( title + " ERROR: LinkedList.ToString(" + title + ") looped more than numElements")
                break

        return p

    def ToStringReversed(self, title:str = "", maxElements:int = -1):
        p = "\n"
        element = self.lastElement
        i = 0
        elements = 0
        while element is not None:
            elements = elements + 1
            if maxElements > 0 and elements > maxElements:
                break

            p += element.ToString() + "\n"
            if element.next == element:
                print(p)
                print_assert(False, "LinkedList.ToString(" + title + ") looped to itself")
            element = element.prev
            i += 1
            if i> self.numElements:
                print( title + " ERROR: LinkedList.ToString(" + title + ") looped more than numElements")
                break

        return p

    def PrintDebug(self, title:str = "", maxElements:int = -1):
        str = self.ToString(title, maxElements)
        print( "LinkedList." + title + " " + str)
    
    def PrintReversedDebug(self, title:str = "", maxElements:int = -1):
        str = self.ToStringReversed(title, maxElements)
        print( "LinkedList.Reversed" + title + " " + str)

    def AddBlock(self, element:LinkedElement):
        self.numElements += 1
        if self.firstElement is None:
            self.firstElement = element
            self.lastElement = element
        else:
            # Update element pointers
            self.lastElement.next = element
            element.prev = self.lastElement

            # Update pointer to last element
            self.lastElement = element

#        print("Adding element", block.ToString())

    def DeleteElement(self, element:LinkedElement):
        if element is None:
            print("ERROR: LinkedList.DeleteElement() element is None")
            return
        
#        print( "DeleteElement:", element.ToString())

        self.numElements -= 1

        if self.firstElement == element:
            self.firstElement = element.next
        if self.lastElement == element:
            self.lastElement = element.prev

        if element.prev is not None:
            element.prev.next = element.next
        if element.next is not None:
            element.next.prev = element.prev

        element.prev = None
        element.next = None

    def InsertAfterBlock(self, thisElement:LinkedElement, newElement:LinkedElement):
        self.numElements += 1

        # Set pointers for the new block
        newElement.next = thisElement.next
        newElement.prev = thisElement
        thisElement.next = newElement

        # Update pointers for the next block
        newElement.FixLinks()

        # Adjust pointer to last block
        if self.lastElement == thisElement:
            self.lastElement = newElement

#        self.PrintDebug("InsertAfterBlock")

    def Swap(self, element1:LinkedElement, element2:LinkedElement):

        # 
        # If the elements are next to eachother  tempPrev1 - element1/tempPrev2 - prevTemp1/element2 - tempNext2
        # If the elements are spaced             tempPrev1 - element1 - tempNext1  ... elements .... tempPrev2 - element2 - tempNext2

        # ---- 8 ---- ----[9]---- ----[10]----  ----11----    ----12----
        # [i8:p7:n9]  [i9:p8:n10][i10:p9:n11]  [i11:p10:n12] [i12:p11:n13]
        # 
        # ---- 8 ---- ----[10]---- ----[9]----   ----11----   ----12----
        # [i9:p8:n10]  [i10:p8:n9] [i9:p10:n11]  [i11:p9:n12] [i12:p11:n13]
        # 
        # ---- 8 ---- ----[11]---- ----[10]----   ----[9]----    ----12----
        # [i8:p7:n9]  [i11:p8:n10] [i10:p9:n11]  [i9:p10:n12] [i12:p11:n13]

        # Special case : Close to eachother : Make sure element1 is first
        if (element2.next == element1 and element1.prev == element2):
#            print( "Swap.Element1IsFirst", element1.ToString(), element2.ToString())
            tempElement = element1
            element1 = element2
            element2 = tempElement
#            print( "Swap.Element1IsFirst", element1.ToString(), element2.ToString())

        # Special case : Close to eachother
        if (element1.next == element2 and element2.prev == element1):
#            print("Swap:Elements are next to eachother")

            # Update pointers
            tempNext = element2.next
            element2.prev = element1.prev
            element2.next = element1
            element1.prev = element2
            element1.next = tempNext

            element1.FixLinks()
            element2.FixLinks()

        else:
            tempPrev1 = element1.prev
            tempNext1 = element1.next
            tempPrev2 = element2.prev
            tempNext2 = element2.next

#            print( "Swap.Element1:", element1.ToString(), element2.ToString())

            # Update pointers
            element1.next = tempNext2
            element1.prev = tempPrev2
            element2.next = tempNext1
            element2.prev = tempPrev1

 #           print( "Swap.Element2:", element1.ToString(), element2.ToString())

            element1.FixLinks()
            element2.FixLinks()

#            print( "Swap.Element3:", element1.ToString(), element2.ToString())
    
        if self.lastElement == element1:
            self.lastElement = element2
        elif self.lastElement == element2:
            self.lastElement = element1
