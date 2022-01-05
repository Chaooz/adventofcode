
from typing import MutableMapping
from advent_libs import print_debug, print_error


class DataPacket:
    instance = 0

    versions : list
    typeId : int
    blocks : list
    children : list
    numbers : list
    results : list
    id = 0

    op_list = {
        (0,"sum"),
        (1," * "),
        (2,"min"),
        (3,"max"),
        (4,"literal"),
        (5,"greater than"),
        (6,"less than"),
        (7,"equal to"),
        (-1,"top node")
    }

    def __init__(self, version = 0, typeId = -1 ):
        DataPacket.instance += 1
        self.id = DataPacket.instance
        self.versions = list()
        self.typeId = typeId
        self.blocks = list()
        self.children = list()
        self.numbers = list()
        self.results = list()

        self.versions.append(version)

    def add_version(self,version):
        self.versions.append(version)

    def add_number(self,number):
        #print_debug("ID:" + str(self.id) + " add number : len(" + str(len(self.numbers)) + ") num:" + str(number))
        self.numbers.append(number)
    
    def add_result(self,number):
        #print_debug("ID:" + str(self.id) + " add result : len(" + str(len(self.results)) + ") num:" + str(number))
        self.results.append(number)


    def add_block(self,txt,data,block):
        #print_debug("ID:" + str(self.id) + " add_block:" + txt + " : " + block)
        self.blocks.append((data,block))
    
    def add_literal_block(self,txt,data,block):
        #print_debug("ID:" + str(self.id) + " add_block:" + txt + " : " + block)
        self.blocks.append((data,block))

    def add_child(self,child_packet):
        if child_packet == self:
            print_error("PACKETERROR")
        self.children.append(child_packet)

    def op_name(self,operator):
        for (id,name) in self.op_list:
            if ( id == operator ):
                return name
        return "?"

    def to_string_flat(self,level):
        b = ""
        l = len(self.children)
        c = ""
        for number in self.numbers:
            c += " " + str(number)

        res = ""
        for number in self.results:
            res += " " + str(number)

        spacer = ""
        if ( level > 0 ):
            spacer += "+"
        for n in range(level):
            spacer += "-"

        if ( self.typeId == 4 ):
            b += spacer +"[ID:" + str(self.id) + "] Children:" + str(l) + " TypeId:" + str(self.typeId) + " number = " + str(self.lit_sum_self()) + " result:" + str(res) + "\n"
        else:
            b += spacer + "[ID:" + str(self.id) + "] Children:" + str(l) + " TypeId:" + str(self.typeId) + " op:" + self.op_name(self.typeId) + " values:" + c + " result: " + str(res) + "\n"
        return b

    def to_string(self, level = 0):
        b = self.to_string_flat(level)
        for child in self.children:
            b += child.to_string(level + 1)
        return b

    def binary_block_string(self):
        binary = ""
        for (o,block) in self.blocks:
            binary += block
        return binary

    def lit_sum_self(self):
        num = 0
        for number in self.numbers:
            num += int(number)
        return num

    def literal_sum(self):
        sum = self.lit_sum_self()

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

    def get_child(self):
        for child in self.children:
            return child
        return None

    def calculate_all(self):
        num = self.calculate_op()
        print_debug(self.to_string())
        return num

    def num_arguments(self):
        return len(self.numbers)

    def get_values(self, min_number, max_number = 999):
        value_list = list()
        num_arguments = self.num_arguments()
        num_args = min(num_arguments,max_number)

        num = 0
        for index in range(0,num_args):
            value = self.numbers[0]
            value_list.append(value)
            self.numbers.pop(0)
            num += 1

        if num < min_number:
            num_results = min(len(self.results),max_number) - num
            
            for _ in range( 0, num_results):
                value = self.results[0]
                value_list.append(value)
                self.results.pop(0)
                num += 1

        if ( num < min_number ):
            print_error("Not enough arguments")

        return value_list

    def do_calculation2(self):
        operation = self.typeId
        sum = 0
        s = ""

        # sum
        if operation == 0:
            value_list = self.get_values(1)
            for value in value_list:
                sum += value
                if len(s) > 0 :
                    s+= " + "
                s += str(value)

        # multiply
        elif operation == 1:
            value_list = self.get_values(1)
            sum = 1
            for value in value_list:
                sum *= value
                if ( len(s) > 0 ):
                    s += " * "
                s += str(value)

        # min 
        elif ( self.typeId == 2):
            value_list = self.get_values(1)
            sum = 999999999999
            for value in value_list:
                sum = min(sum,value)               
                s += " min " + str(value)

        # max 
        elif ( self.typeId == 3):
            value_list = self.get_values(1)
            sum = -999999999999
            for value in value_list:
                sum = max(sum,value)               
                s += " max " + str(value)

        # Greater than (always 2 args)
        elif ( self.typeId == 5):
            value_list = self.get_values(2,2)
            if len ( value_list ) == 2:
                value1 = value_list[0]
                value2 = value_list[1]

                s += str(value1) + " > " + str(value2)
                if value1 > value2:
                    sum = 1
                else:
                    sum = 0
        # Less than
        elif ( self.typeId == 6):
            value_list = self.get_values(2,2)
            if len ( value_list ) == 2:
                value1 = value_list[0]
                value2 = value_list[1]

                s += str(value1) + " < " + str(value2)
                if value1 < value2:
                    sum = 1
                else:
                    sum = 0
                
        # Equal to
        elif ( self.typeId == 7):

            value_list = self.get_values(2,2)
            if len ( value_list ) == 2:
                value1 = value_list[0]
                value2 = value_list[1]
                s += str(value1) + " eq " + str(value2)
                if value1 == value2:
                    sum = 1
                else:
                    sum = 0

        elif operation == -1:
            return None
        else:
            print_error("Not implemented OP:" + str(self.typeId) + ":" + str(self.op_name(self.typeId)))
            return None
        print_debug("ID:" + str(self.id) + " do_calculation[" + str(operation) + ":" + str(self.op_name(operation)) + "] : " + str(s) + " = " + str(sum))
        return sum

    def move_result(self,parent):
        for number in self.numbers:
            #print_debug("ID:" + str(self.id) + " remove number : " + str(number))
            parent.add_result(number)

        for result in self.results:
            #print_debug("ID:" + str(self.id) + " remove result : " + str(result))
            parent.add_result(result)

        self.numbers.clear()        
        self.results.clear()

    def get_result(self):
        if len(self.results) == 1:
            for result in self.results:
                return result
        return None

    def calculate_op(self):
        #if not self.typeId == 4:

        for child in self.children:
            child.calculate_op()
            child.move_result(self)
        a = self.do_calculation2()
        if a != None:
#            self.add_result(a)
            self.add_number(a)
            return a
        return self.get_result()
            
            
#            if len(new_stack) > 0:
#                value1 = new_stack.pop(0)
#                sum = self.do_calculation(self.typeId,value1,new_stack)
#                stack.append(sum)
#                for p in new_stack:
#                    stack.append(p)
#            else:
#                print("StackError:" + str(len(new_stack)))
                
        
