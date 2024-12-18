from sys import stdin

registers, memory = stdin.read().strip().split('\n\n')

m_stack = [int(m) for m in memory.replace('Program: ', "").split(',')]

ins_pointer = 0

opcodes = {value: op for value, op in enumerate(['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv'])}

operands = {
        0: "#0",
        1: "#1",
        2: "#2",
        3: "#3",
        4: "A",
        5: "B",
        6: "C",
        7: Exception(),
        }

while ins_pointer != len(m_stack):
    opcode = opcodes[m_stack[ins_pointer]]
    """
    The adv instruction (opcode 0) performs division. The numerator is the
    value in the A register. The denominator is found by raising 2 to the power
    of the instruction's combo operand. (So, an operand of 2 would divide A by
                                         4 (2^2); an operand of 5 would divide
                                         A by 2^B.) The result of the division
    operation is truncated to an integer and then written to the A register.
    """
    literal_operand = m_stack[ins_pointer + 1]
    combo_operand: str = operands[literal_operand]
    match opcode:
        case 'adv':
            print(f"A = A / {combo_operand}")
        case 'bxl':
            """
            The bxl instruction (opcode 1) calculates the bitwise XOR of register B
            and the instruction's literal operand, then stores the result in
            register B.
            """
            print(f"B = B ^ {literal_operand}")
        case "bst":
            """
            The bst instruction (opcode 2) calculates the value of its combo
            operand modulo 8 (thereby keeping only its lowest 3 bits), then writes
            that value to the B register.
            """
            print(f"B = {combo_operand} % 8")
        case "jnz":
            """
            The jnz instruction (opcode 3) does nothing if the A register is 0.
            However, if the A register is not zero, it jumps by setting the
            instruction pointer to the value of its literal operand; if this
            instruction jumps, the instruction pointer is not increased by 2 after
            this instruction.
            """
            print(f"jnz {literal_operand}")
        case "bxc":
            """
            The bxc instruction (opcode 4) calculates the bitwise XOR of register B
            and register C, then stores the result in register B. 
            (For legacy reasons, this
             instruction reads an operand but ignores it.)
            """
            print(f"B = B ^ C")
        case "out":
            print(f"out {combo_operand} % 8")
        case "bdv":
            print(f"B = A / {combo_operand}")
        case "cdv":
            print(f"C = A / {combo_operand}")
        case _:
            raise NotImplemented(opcode)
    ins_pointer += 2

