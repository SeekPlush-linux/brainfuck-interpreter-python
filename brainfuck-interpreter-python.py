import sys, os
if os.name == "nt":
    import msvcrt
else:
    import tty, termios

memory_size = 30000  # Number of cells
cell_size   = 255    # Max number each cell can reach

global memory
global selected
memory = [0]*memory_size
selected = 0
loop_stack = []
current_op_idx = -1

def getch():
    if os.name == "nt":
        ch = msvcrt.getch().decode("utf-8")
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def execute_bf_code(code):
    global memory
    global selected
    loop_stack = []
    current_op_idx = -1

    while True:
        current_op_idx += 1
        try:
            op = code[current_op_idx]
        except IndexError:
            break

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
                return 130
            elif user_input == '\x04':
                print()
                return 1
            memory[selected] = ord(user_input) % (cell_size+1)

        # . - Prints 1 character from selected cell
        if op == ".":
            print(chr(memory[selected]), end="", flush=True)
    return 0

args = sys.argv
if len(args) > 1:
    code = " ".join(args[1:])
    exit(execute_bf_code(code))
else:
    from prompt_toolkit import prompt
    from prompt_toolkit.history import InMemoryHistory
    history = InMemoryHistory()
    print("Brainfuck 1.0.0 (30 Jun 2025)")
    print("Press Ctrl+C or Ctrl+D to exit.")
    while True:
        try:
            code = prompt(">>> ", history=history)
        except (KeyboardInterrupt, EOFError):
            exit(0)
        execute_bf_code(code)
