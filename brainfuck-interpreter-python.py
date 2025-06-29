import sys, termios, tty

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

args = sys.argv
if len(args) > 1:
    code = " ".join(args[1:])
else:
    code = input("Enter brainfuck code: ")

memory_size = 30000  # Number of cells
cell_size   = 255    # Max number each cell can reach

memory = [0]*memory_size
selected = 0
loop_stack = []
current_op_idx = -1

while True:
    current_op_idx += 1
    try:
        op = code[current_op_idx]
    except IndexError:
        break
    # print(selected, loop_stack, current_op_idx, memory[selected], code[current_op_idx])

    # < - Moves pointer 1 cell to the left
    if op == "<":
        selected -= 1
        if selected < 0:
            selected = memory_size - 1

    # > - Moves pointer 1 cell to the right
    if op == ">":
        selected += 1
        if selected > memory_size - 1:
            selected = 0

    # + - Adds 1 to the selected cell
    if op == "+":
        memory[selected] += 1
        if memory[selected] > cell_size:
            memory[selected] = 0

    # - - Subtracts 1 from the selected cell
    if op == "-":
        memory[selected] -= 1
        if memory[selected] < 0:
            memory[selected] = cell_size

    # [ - Starts a `while selected != 0` loop
    if op == "[":
        if memory[selected] == 0:
            while True:
                current_op_idx += 1
                if code[current_op_idx] == "]":
                    current_op_idx += 1
                    break
            continue
        loop_stack.insert(0, current_op_idx)

    # ] - End of loop; if the selected cell isn't equal to zero, go back to the corresponding "["
    if op == "]":
        if memory[selected] != 0:
            current_op_idx = loop_stack[0]
            continue
        loop_stack.pop(0)

    # , - Awaits for user input of 1 character
    if op == ",":
        user_input = getch()
        if user_input == '\x03':
            print()
            exit(130)
        elif user_input == '\x04':
            print()
            exit(1)
        memory[selected] = ord(user_input) % (cell_size+1)

    # . - Prints 1 character from selected cell
    if op == ".":
        print(chr(memory[selected]), end="", flush=True)
