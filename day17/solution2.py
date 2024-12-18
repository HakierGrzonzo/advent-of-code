from sys import stdin
import multiprocessing
from itertools import count
import sys

registers, memory = stdin.read().strip().split('\n\n')

m_stack = [int(m) for m in memory.replace('Program: ', "").split(',')]


opcodes = {value: op for value, op in enumerate(['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv'])}

def simulate_a(a: int):
    ins_pointer = 0
    output = []
    r_state = {
        'A': a,
        'B': 0,
        'C': 0 
    }
    operands = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3,
            4: lambda: r_state['A'],
            5: lambda: r_state['B'],
            6: lambda: r_state['C'],
            7: lambda: Exception(),
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
        combo_operand: int = operands[literal_operand]()
        match opcode:
            case 'adv':
                denominator = 2 ** combo_operand
                numerator = r_state['A']
                r_state['A'] = int(numerator / denominator)
            case 'bxl':
                """
                The bxl instruction (opcode 1) calculates the bitwise XOR of register B
                and the instruction's literal operand, then stores the result in
                register B.
                """
                r_state['B'] = r_state['B'] ^ literal_operand
            case "bst":
                """
                The bst instruction (opcode 2) calculates the value of its combo
                operand modulo 8 (thereby keeping only its lowest 3 bits), then writes
                that value to the B register.
                """
                r_state['B'] = combo_operand % 8
            case "jnz":
                """
                The jnz instruction (opcode 3) does nothing if the A register is 0.
                However, if the A register is not zero, it jumps by setting the
                instruction pointer to the value of its literal operand; if this
                instruction jumps, the instruction pointer is not increased by 2 after
                this instruction.
                """
                if r_state['A'] != 0:
                    ins_pointer = literal_operand
                    continue
            case "bxc":
                """
                The bxc instruction (opcode 4) calculates the bitwise XOR of register B
                and register C, then stores the result in register B. 
                (For legacy reasons, this
                 instruction reads an operand but ignores it.)
                """
                r_state['B'] = r_state['B'] ^ r_state['C']
            case "out":
                output.append(combo_operand % 8)
            case "bdv":
                denominator = 2 ** combo_operand
                numerator = r_state['A']
                r_state['B'] = int(numerator / denominator)
            case "cdv":
                denominator = 2 ** combo_operand
                numerator = r_state['A']
                r_state['C'] = int(numerator / denominator)
            case _:
                raise NotImplemented(opcode)
        ins_pointer += 2
    return output

def solve(start, goal):
    if not goal:
        yield start // 8
    for trial in range(start, start+8):
        if simulate_a(trial)[0] == goal[-1]:
            yield from solve(trial * 8, goal[:-1])

for sol in solve(0, m_stack):
    assert simulate_a(sol) == m_stack
    print(sol)
    break
