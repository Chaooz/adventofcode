import itertools, sys
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def left_to_right_eval(numbers, ops):
    """Evaluate the expression defined by `numbers` and `ops` strictly left-to-right,
    where ops can be '+', '*', or '||'.
    """
    # Start with the first number
    result = numbers[0]
    for op, num in zip(ops, numbers[1:]):
        if op == '+':
            result = result + num
        elif op == '*':
            result = result * num
        else:  # op == '||' (concatenation)
            # Convert to strings, concatenate, then convert back to int
            result = int(str(result) + str(num))
    return result

def can_form_target(numbers, target):
    """Check if we can insert +, *, or || between numbers (in order) to form the target,
    evaluating strictly left-to-right."""
    if len(numbers) == 1:
        return numbers[0] == target

    operators = ['+', '*', '||']
    for ops in itertools.product(operators, repeat=len(numbers)-1):
        if left_to_right_eval(numbers, ops) == target:
            return True
    return False

def solve_puzzle(filename):
    lines = loadfile(filename)
    total = 0
    for line in lines:
        target_str, nums_str = line.split(':')
        target = int(target_str.strip())
        numbers = list(map(int, nums_str.split()))
        if can_form_target(numbers, target):
            total += target
    return total

print(f"Total calibration result: {solve_puzzle('input.txt')}")
