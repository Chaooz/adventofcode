
from typing import MutableMapping
from advent_libs import print_debug, print_error, print_assert
from math import prod

class DataPacket:
    instance = 0

    versions : list
    typeId : int
    blocks : list
    children : list
    numbers : list
    results : list
    id = 0

    op_block_length = 0
    op_block_number = 1

    op_list = {
        (0," + "),
        (1," * "),
        (2,"min"),
        (3,"max"),
        (4,"literal"),
        (5," > "),
        (6," < "),
        (7,"equal to"),
        (-1,"noop")
    }

    def __init__(self, version = 0, typeId = -1 ):
        DataPacket.instance += 1
        self.id = DataPacket.instance
        self.versions = list()
        self.typeId = typeId
        self.blocks = list()
        self.children = list()
        self.numbers = list()
        self.value = 0
        self.results = list()
        self.versions.append(version)

    def set_value(self,value):
        self.value = value

    def get_values(self):
        values = list()
        for child in self.children:
            values.append(child.value)
        return values

    def add_block(self,block_type,data,block):
        #print_debug("ID:" + str(self.id) + " add_block:" + str(block_type) + " : " + block)
        self.blocks.append((block_type,data,block))
    
    def add_children(self,child_list):
        self.children = child_list

    def op_name(self,operator):
        for (id,name) in self.op_list:
            if ( id == operator ):
                return name
        return "?"

    def to_string_flat(self,level):
        b = ""
        l = len(self.children)

        res = ""
        for number in self.results:
            res += " " + str(number)

        spacer = ""
        if ( level > 0 ):
            spacer += "+"
        for n in range(level):
            spacer += "-"

        b += spacer + "[ID:" + str(self.id) + "] Children:" + str(l) + " TypeId:" + str(self.typeId) + " op:" + self.op_name(self.typeId) + " value:" + str(self.value) + " result: " + str(res) + "\n"
        return b

    def to_string(self, level = 0):
        b = self.to_string_flat(level)
        for child in self.children:
            b += child.to_string(level + 1)
        return b

    def literal_sum(self):
        sum = self.value
        for child in self.children:
            sum += child.literal_sum()
        return sum

    def version_sum(self):
        sum = 0
        for version in self.versions:
            sum += version

        for child in self.children:
            sum += child.version_sum()
        return sum

    def do_calculation(self):
        operation = self.typeId
        s = ""
        value = 0

        if operation <= 3:
            value_list = self.get_values()

            for number in value_list:
                if ( len(s) > 0 ):
                    s += " " + self.op_name(operation) + " "
                s += str(number)

            if operation == 0:
                value = 0
                for number in value_list:
                    value += number
            elif operation == 1:
                value = prod(value_list)
            elif ( operation == 2):
                value = min(value_list)
            elif ( operation == 3):
                value = max(value_list)
            else:
                print_assert(False,"Unknown operation : " + str(operation))

        elif operation == 4:
            return None
        else:
            value_list = self.get_values()
            print_assert(len(value_list) > 1,"Requires at least 2 arguments : " + str(value_list))
            value1 = value_list[0]
            value2 = value_list[1]
            s += str(value1) + " " + self.op_name(operation) + " " + str(value2)

            if ( self.typeId == 5):
                value = value1 > value2
            elif ( self.typeId == 6):
                value = value1 < value2                     
            elif ( self.typeId == 7):
                value = value1 == value2

            value = int(value)

        #print_debug("ID:" + str(self.id) + " do_calculation[" + str(operation) + ":" + str(self.op_name(operation)) + "] : " + str(s) + " = " + str(value))
        return value

    def calculate_all(self):
        for child in self.children:
            if child.typeId != 4:
                value = child.calculate_all()
                child.set_value(value)

        return self.do_calculation()
