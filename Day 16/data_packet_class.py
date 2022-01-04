
class DataPacket:
    version = int()
    typeId = int()
    blocks = list()
    children = list()
    numbers = list()

    op_list = {
        (0,"sum"),
        (1," * "),
        (2,"min"),
        (3,"max"),
        (4,"literal"),
        (5,"greater than"),
        (6,"less than"),
        (7,"equal to")
    }

    def __init__(self, version, typeId ):
        self.version = version
        self.typeId = typeId
        self.blocks = list()
        self.children = list()

    def add_number(self,number):
        self.numbers.append(number)

    def add_block(self,txt,data,block):
        #print("add_block:" + txt + " : " + block)
        self.blocks.append((data,block))

    def add_child(self,child_packet):
        self.children.append(child_packet)

    def op_name(self,operator):
        for (id,name) in self.op_list:
            if ( id == operator ):
                return name
        return "?"

    def to_string_flat(self):
        b = ""
        l = len(self.children)
        if ( self.typeId == 4 ):
            b += "C:" + str(l) + " T:" + str(self.typeId) + " number = " + str(self.lit_sum_self()) + "\n"
        else:
            b += "c:" + str(l) + " T:" + str(self.typeId) + " op:" + self.op_name(self.typeId) + "\n"
        return b

    def to_string(self):
        b = self.to_string_flat()
        for child in self.children:
            b += child.to_string()
        return b

    def binary_block_string(self):
        binary = ""
        for (o,block) in self.blocks:
            binary += block
        return binary

    def lit_sum_self(self):
        string = self.binary_block_string()
        if len(string) > 0 :
            n = int(string,2)
            return n
        return 0
        #return 0

    def literal_sum(self):
        sum = 0
        if self.typeId == 4:
            sum += self.lit_sum_self()

        for child in self.children:
            sum += child.literal_sum()

#        for num in self.numbers:
#            sum += num

        return sum

    def version_sum(self):
        sum = self.version
        for child in self.children:
            sum += child.version_sum()
        return sum

    def get_child(self):
        for child in self.children:
            return child
        return None

    def calculate_all(self):
        stack = list()
        self.calculate_op(stack)
        print(stack)
        if (len(stack) == 1):
            return stack.pop()

    def do_calculation(self, operation, value1, stack):
        sum = -1
        s = ""
        # sum
        if operation == 0:
            sum = value1
            if(len(stack) > 0):
                value2 = stack.pop(0)
                sum += value2
                s += " + " + str(value2)
        # multiply
        elif ( self.typeId == 1):
            sum = value1
            if(len(stack) > 0):
                value2 = stack.pop(0)
                sum *= value2
                s += " * " + str(value2)
        # min 
        elif ( self.typeId == 2):
            sum = value1
            while(len(stack) > 0):
                value2 = stack.pop(0)
                sum = min(sum,value2)               
                s += " min " + str(value2)

        # max 
        elif ( self.typeId == 3):
            sum = value1
            while(len(stack) > 0):
                value2 = stack.pop(0)
                sum = max(sum,value2)               
                s += " max " + str(value2)
        # Noop
        elif self.typeId == 4:
            sum = 0
        # Greater than (always 2 args)
        elif ( self.typeId == 5):
            value2 = stack.pop(0)
            s += " > " + str(value2)
            if value1 > value2:
                sum = 1
            else:
                sum = 0
        # Less than
        elif ( self.typeId == 6):
            value2 = stack.pop(0)
            s += " < " + str(value2)
            if value1 < value2:
                sum = 1
            else:
                sum = 0
        # Equal to
        elif ( self.typeId == 7):
            value2 = stack.pop(0)
            s += " == " + str(value2)
            if value1 == value2:
                sum = 1
            else:
                sum = 0
        else:
            print("Not implemented OP:" + str(self.typeId) + ":" + str(self.op_name(self.typeId)))
            return -1
        print("do_calculation[" + str(operation) + "] : " + str(value1) + str(s) + " = " + str(sum))
        return sum

    def calculate_op(self, stack:list):
        if not self.typeId == 4:
            new_stack = list()
            for child in self.children:
                child.calculate_op(new_stack)
            
            if len(new_stack) > 0:
                value1 = new_stack.pop(0)
                sum = self.do_calculation(self.typeId,value1,new_stack)
                stack.append(sum)
                for p in new_stack:
                    stack.append(p)
            else:
                print("ERR" + str(len(new_stack)))
                
        elif self.typeId == 4:
            value1 = self.lit_sum_self()
            stack.append(value1)
            for child in self.children:
                child.calculate_op(stack)
        else:
            print("WHAT?")
        
