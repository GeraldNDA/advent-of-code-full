class OpCode():
    
    @staticmethod
    def perform_op(opcode, regA, regB, regC, registers=[]):
        op1 = None
        op2 = None
        operator = None

        if opcode[:-1] in OpCode.MODIFIER_OPS:
            op1 = registers[regA]
            if opcode[-1] == 'i':
                op2 = regB
            elif opcode[-1] == 'r':
                op2 = registers[regB]
            operator = OpCode.MODIFIER_OPS[opcode[:-1]]
        
        elif opcode[:-1] in OpCode.ASSIGNMENT_OPS:
            if opcode[-1] == 'i':
                op1 = regA
            elif opcode[-1] == 'r':
                op1 = registers[regA]
            operator = OpCode.ASSIGNMENT_OPS[opcode[:-1]]

        elif opcode[:-2] in OpCode.COMPARISON_OPS:
            if opcode[-2] == "r":
                op1 = registers[regA]
            elif opcode[-2] == "i":
                op1 = regA
            if opcode[-1] == "r":
                op2 = registers[regB]
            elif opcode[-1] == "i":
                op2 = regB
            operator = OpCode.COMPARISON_OPS[opcode[:-2]]
        try:
            registers[regC] = operator(op1, op2)
        except Exception as e:
            print()
            print(e, opcode, registers)
            raise ValueError
    
    @staticmethod
    def get_all_ops():
        for operator in set(OpCode.ASSIGNMENT_OPS) | set(OpCode.MODIFIER_OPS):
            yield operator + "i"
            yield operator + "r"
        
        for operator in set(OpCode.COMPARISON_OPS):
            yield operator + "ir"
            yield operator + "ri"
            yield operator + "rr"

    @staticmethod
    def add(op1, op2):
        return op1 + op2
    @staticmethod
    def mul(op1, op2):
        return op1 * op2
    @staticmethod
    def ban(op1, op2):
        return op1 & op2
    def bor(op1, op2):
        return op1 | op2
    
    @staticmethod
    def set(op1, op2):
        return op1
    
    @staticmethod
    def gt(op1, op2):
        return int(op1 > op2)
    
    @staticmethod
    def eq(op1, op2):
        return int(op1 == op2)


OpCode.COMPARISON_OPS ={
    "gt": OpCode.gt,
    "eq": OpCode.eq
}
OpCode.MODIFIER_OPS = {
    "add": OpCode.add,
    "mul": OpCode.mul,
    "ban": OpCode.ban,
    "bor": OpCode.bor,
}
OpCode.ASSIGNMENT_OPS = {
    "set": OpCode.set
}