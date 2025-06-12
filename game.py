import random

def generate(num_cnt, level):
    """
    Generate a mathematical expression that evaluates to 24 using num_cnt random numbers and level difficulty.

    :param num_cnt: The number of random numbers to use (default=4)
    :param level: The difficulty level (1 or 2), where:
        - 1 only uses addition (+) and subtraction (-)
        - 2 uses addition, subtraction, multiplication (*), and division (/)
    :return: A string representing the mathematical expression
    """
    if num_cnt < 4:
        raise ValueError("num_cnt must be at least 4")

    # Generate random numbers within [1, 13]
    nums = [random.randint(1, 13) for _ in range(num_cnt)]

    # Initialize the expression with the first number
    expr = str(nums[0])

    # Add operations based on the difficulty level
    if level == 2:
        ops = ['*', '/', '+', '-']
    else:  # level == 1
        ops = ['+', '-']

    for i in range(1, num_cnt):
        op = random.choice(ops)
        expr += f" {op} {str(nums[i])}"

    # Ensure the expression evaluates to 24
    if eval(expr) != 24:
        return generate(num_cnt, level)

    return expr + " = 24"

# print(generate(4, 1))  # Example output: "6 * 8 * 3 / 6 = 24"