import copy
# add python-constraint to the project-interpreter by going to settings-->project interpreter--> press the +
# --> search for "python-constraint" and press "install packages"
from constraint import *

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
                vertical_vars[count].append('')
            else:
                if x[-1] == '_':
                    x.pop()
                    vertical_vars[count].append('==')
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
# TODO currently only supports transfer for addition. Other Operations have to be implemented
def create_equations():
    global global_vv
    global global_oo
    equation = []

    counter = 0
    for x in global_vv:
        single_eq = list()   # represents a single equation of a vertical alignment
        if counter != 0:            # check if counter is zero since the rightmost equation doesn't have a transfer
            single_eq.append('x' + str(counter) + '+')  # adds a transfer variable to the equation. transfer is later determined from floor(last vertical alignment without result /10)
        for i in range(len(x)):
            if x[i] == '':  # if one word is longer than another a '' gets injected as placeholder. This must be replaced by 0
                single_eq.append('0')   # replacing ''
            else:
                single_eq.append(x[i])      # if there is nothing to replace, append the given value
            if i < len(global_oo):  # if i is not the last index for the list
                single_eq.append(global_oo[i])  # add the operation-sign from the operations order
        equation.append(''.join(single_eq))     # append the part-equation to the list of all equations.
        counter += 1    # increment the counter for the transfer-variables
    return equation


# the separated equations
global_eq = create_equations()
# printing global variables
print(global_oo)  # oo = operation order
print(global_vd)  # vd = variable dictionary
print(global_vv)  # vv = vertical variables --> represents the variables in vertical alignment
print(global_eq)  # eq = equations
print(content)  # filtered content, at the moment includes just the variables as well as one list/line of underscores '_'

# -----------------------------------------------------------------------------------------------
#


# this function divides the variables/letters into two sets, since the letters at the first position of each word are
# not allowed to be zero
def calc_first_vars():
    global content
    content = [[elem for elem in x if elem != '_'] for x in content]    # removes the '_' from content
    variables = [set(), set()]  # first set represents vars not allowed to be zero, second sets vars are allowed to be zero
    for x in content:   # for every word in the equation
        for i in range(len(x)):     # for every letter of each word
            if i == 0:              # check if this letter is at index 0 (first letter)
                variables[0].add(x[i])      # if yes: add it to the first set of letters
                if x[i] in variables[1]:    # check if the letter is also in the second set
                    variables[1].discard(x[i])  # if yes: delete it from the second set
            else:                           # else
                if x[i] not in variables[0]:    # check if the letter is not in the first set
                    variables[1].add(x[i])      # if this is true: add it to the second set of letters
    return variables


global_nzz = calc_first_vars()    # nzz = not zero zero --> a list of 2 sets, first one represents the vars that are
# not allowed to be zero, the second one represents the rest
print(global_nzz)


# adds all variables and its domains to a given problem
def add_vars_to(problem):
    global global_nzz
    global global_vv
    for i in range(len(global_nzz)):
        if i == 0:
            for x in global_nzz[i]:
                problem.addVariable(x, [1, 2, 3, 4, 5, 6, 7, 8, 9])     # adding variables with domains that do not include zero
        else:
            for x in global_nzz[i]:
                problem.addVariable(x, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # adding variables with domains that do include zero
    for i in range(len(global_vv)+1):
        problem.addVariable('x'+str(i), [0, 1, 2, 3, 4])   # adding transfer-variables with the domains 0-3 (at least for now)



# adds all constraints to a given problem
def add_constraints_to(problem):
    global global_vv    # declaring global_vv as global for this function
    global global_eq    # declaring global_eq as global for this function
    global global_oo    # declaring global_oo as global for this function
    global_vv = [[elem for elem in x if elem != '=='] for x in global_vv]    # filtering '==' from global_vv
    print(global_vv)
    vertvars = []   # declaring a local list save the data
    for x in global_vv:     # for every vertical alignment do:
        single = ''     # declaring a local string as a temporary variable
        for i in range(len(x)):     # for every element in a vertical alignment
            if x[i] != '':      # if a element is not empty. Empty elements occur if one word in the equation is longer than another.
                if i == len(x)-1:       # if i is the index of the last element in a vertical alignment, meaning the result line
                    single = single + x[i]      # add that result into to the single variable
                else:   # if not
                    single = single + x[i] + ', '   # add the element and a ', ' to the single variable
        vertvars.append(single)     # append a vertical alignment to the vertvars list. result is that
        # the vertical alignment as a list of lists is converted to a list of strings.
    print(vertvars)     # print vertvars for debugging
    vertvars_set = [set(x) for x in vertvars]   # creates a list of sets of all vertical variables
    for x in vertvars_set:  #
        if ' ' in x:        #
            x.remove(' ')   # removing unwanted characters that are in the data due to String representation
        if ',' in x:        #
            x.remove(',')   #
    vertvars_pseudoset = [list(x) for x in vertvars_set]    # converts the sets back to lists due to contracts later (addConstraint does not accept sets)
    for i in range(len(vertvars_pseudoset)):
        if i != 0:
            vertvars_pseudoset[i].append('x' + str(i))
    print(vertvars_pseudoset)       # print for debugging
    for i in range(len(vertvars_pseudoset)):    # iterate over vertvars_pseudoset to add the constraints to the problem
        print('xxx')                        #
        print(global_eq[i])                 # Prints for debugging
        print(vertvars_pseudoset[i])        #
        problem.addConstraint(lambda a, b, c, d: eval(global_eq[i]), vertvars_pseudoset[i])      # --> adding the constraints for the equations.
    eq_wo_result = list()       # read: equation without result --> used for the transfer constraints
    for x in global_eq:
        single_eq = ''  # a single equation without a result
        for y in x:     # for every letter in the string
            if y == '=':    # if y equals '='
                break       # break, because after '=' there is only the result left, what we don't want in our equation
            else:           # else
                single_eq = single_eq + y       # add the value (it's either a variable or a operation sign) to the single_eq string
        eq_wo_result.append(single_eq)      # append the single_eq to the list of equations without a result
    print(eq_wo_result)     # print for debugging
    for i in range(len(eq_wo_result)):
        eq_wo_result[i] = eq_wo_result[i] + '==' + 'x' + str(i+1)   # add transfer-variables to the equation
    print(eq_wo_result)     # print for debugging
    for i in range(len(eq_wo_result)):  # for every equation that is relevant for the transfer
        vertvars_pseudoset[i].append('x' + str(i))      # add the transfer variable to the variables
        problem.addConstraint(lambda x: math.floor(eval(eq_wo_result[i])/10), vertvars_pseudoset[i])  # add the constraints to the problem with the equations and the variables
        # TODO lambda function requires the exact amount of variables as in the equation and they have to be named exactly the same way as in the domain-variables for the constraints. 


# function to solve the problem
def solve():
    problem = Problem()
    add_vars_to(problem)
    add_constraints_to(problem)

    # ab hier ist kaka:
    #problem.addVariable("THREE", range(10000, 99999))
    #problem.addVariable("FIVE", range(1000, 9999))
    #problem.addVariable("ELEVEN", range(100000, 999999))
    #problem.addConstraint(lambda a, b, c, d: a + b + c == d, ["THREE", "THREE", "FIVE", "ELEVEN"])

    #problem.addConstraint(AllDifferentConstraint())
    return problem.getSolutions()


print(solve())
