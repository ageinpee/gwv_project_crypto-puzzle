import copy
# Exercise 11.3: Cryptoarithmetical Puzzle
# opening a text file with exactly one crypto-puzzle in it
with open("crypto-puzzle-data.txt", encoding="utf-8") as f:
    content = f.readlines()


# function to format the file
# formatting the file into a usable form.
# first of all a the complete string is divided into substring consisting of exactly one line in the file.
# second these substrings are transformed into a list of chars.
# third all useless characters like ' ' are removed
def format_input(con):
    con = [x.strip() for x in con]
    con = [list(x) for x in con]
    con = [[elem for elem in x if elem != ' '] for x in con]
    return con


# formatting the content
content = format_input(content)


# function to define the order of operations.
# function iterates over the list of character(content) and checks if one of these characters is an operation
# if this is true, this operations sign is added to the op_order list.
# currently not implemented: prioritising point over line operations
def create_operation_order(con):
    op_order = []
    for x in con:
        for y in x:
            if y == '+' or y == '-' or y == '*' or y == '/':
                op_order.append(y)
    return op_order


# creating the operations order
global_oo = create_operation_order(content)


# filtering all operation symbols from the content
# '+', '-', '*' and '/' are removed
def filter_operations(con):
    con = [[elem for elem in x if elem != '+'] for x in con]
    con = [[elem for elem in x if elem != '-'] for x in con]
    con = [[elem for elem in x if elem != '*'] for x in con]
    con = [[elem for elem in x if elem != '/'] for x in con]
    return con


# filtering operation symbols
content = filter_operations(content)


# creates a dictionary of the variables in the puzzle so that every variable is a key in the dictionary
# underscore lines ('_') are removed from the dict
# this dictionary can be used to save the possible solutions for a puzzle. If there are more than one solution they can be added to the list
def create_vars(con):
    var_dict = {}
    for x in con:
        for y in x:
            if y not in var_dict.keys():
                var_dict[y] = []
    var_dict.pop('_', None)
    return var_dict


# creating the variable dictionary
global_vd = create_vars(content)


# creating a list of lists with all the vertical alignments in the equation
# uses the pop() function to get the last element of every sublist.
# If a list is empty ' ' is added instead, if the element is '_' a '=' is added instead. 
# first element is the right-most alignment
def create_vertical_vars(con):
    vertical_vars = []
    count = 0
    for i in range(len(max(con, key=len))):
        vertical_vars.append([])
        for x in con:
            if not x:
                vertical_vars[count].append(' ')
            else:
                if x[-1] == '_':
                    x.pop()
                    vertical_vars[count].append('=')
                else:
                    vertical_vars[count].append(x.pop())
        count += 1
    return vertical_vars


# copying the values of content to another variable to keep the data after getting the vertical alignments
vv_content = copy.deepcopy(content)
# creating a list of lists of the vertical alignments in the equation
global_vv = create_vertical_vars(vv_content)


# creates equations from the vertical alignment.
# for this the vertical alignment and operations order are used.
def create_equations():
    global global_vv
    global global_oo
    equation = []
    for x in global_vv:
        single_eq = []
        for i in range(len(x)):
            single_eq.append(x[i])
            if i < len(global_oo):
                single_eq.append(global_oo[i])
        equation.append(single_eq)
    return equation


global_eq = create_equations()

# printing global variables
print(global_oo)  # oo = operation order
print(global_vd)  # vd = variable dictionary
print(global_vv)  # vv = vertical variables --> represents the variables in vertical alignment
print(global_eq)  # eq = equations
print(content)  # filtered content, at the moment includes just the variables as well as one list/line of underscores '_'


