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
def create_vars(con):
    var_dict = {}
    for x in con:
        for y in x:
            if y not in var_dict.keys():
                var_dict[y] = 0
    var_dict.pop('_', None)
    return var_dict


# creating the variable dictionary
global_vd = create_vars(content)


# creating a list of lists with all the vertical alignments in the equation
#def create_vertical_vars(con):
#    vertical_vars = []
#    flag = False
#    for x in con:
#        if len(x) < len(max(con,key=len)):
#            for i in range(0, len(max(con,key=len))-len(x)):
#                if flag == False:
#                    vertical_vars.append([x[' ']])
#                if flag == True:
#                    vertical_vars[].append()
#        for i in range(len(x)-1, 0):
#            if flag == False:
#                vertical_vars.append([x[i]])



# printing global variables
print(global_oo)
print(global_vd)
print(content)
