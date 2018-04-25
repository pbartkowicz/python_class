import string

# Minimizes the given expression with Quine-McCluskey algorithm

# | - or
# & - and
# ^ - xor
# ~ - not
# > - conditional
# = - iff (if and only if)


def validate(expr):

    alphanum = "".join(string.ascii_letters) + "".join(string.digits)
    operators = "|&^>="
    state = 0
    count = 0           # how many brackets were used
    new_expr = []
    variables = set()
    argument = ""

    for char in expr:

        if char == " ":
            continue

        if state == 0:                  # waits for (, ~ or arg after beginning, (, arg, operator

            if char == "(":
                count += 1
            elif char == "~":
                state = 1
            elif char in alphanum:
                state = 2
                argument += char
            else:
                return [False, False]

        elif state == 1:                # waits for ( or arg after ~

            if char == "(":
                state = 0
                count += 1
            elif char in alphanum:
                state = 2
                argument += char
            else:
                return [False, False]

        elif state == 2:                # waits for ), operator or arg after arg

            if char == ")":
                count -= 1
                state = 3
            elif char in operators:
                state = 0
            elif char in alphanum:
                state = 2
                argument += char
            else:
                return [False, False]

            if state in [0, 3]:
                new_expr.append(argument)
                variables.add(argument)
                argument = ""

        elif state == 3:                # waits for operator or ) after )

            if char in operators:
                state = 0
            elif char == ")":
                count -= 1
            else:
                return [False, False]

        if state in [0, 1, 3]:
            new_expr.append(char)

        if count < 0:
            return [False, False]

    if count == 0 and state in [2, 3]:

        if state == 2:                  # add the argument from the end of the expression
            new_expr.append(argument)
            variables.add(argument)

        return [new_expr, variables]

    else:
        return [False, False]


# converts the given expression to rpn notation


def to_rpn(new_expr, variables):

    rpn_expr = []
    stack = []

    for char in new_expr:

        if char in variables:
            rpn_expr.append(char)

        elif char == "(":
            stack.append(char)

        elif char == ")":
            while len(stack) != 0 and stack[-1] != "(":
                rpn_expr.append(stack.pop())
            stack.pop()

        else:
            while len(stack) != 0 and stack[-1] != "(":

                if (char in ">=" and stack[-1] in ">=") or (char in "|&^" and stack[-1] in "~|&^"):
                    rpn_expr.append(stack.pop())
                    continue
                break

            stack.append(char)

    while stack:
        rpn_expr.append(stack.pop())

    return rpn_expr


# creates the bit masks for all possible combinations


def create_mask(args_num):

    length = 2 ** args_num
    mask = []

    for i in range(length):

        bin_value = bin(i)
        bin_value = [int(x) for x in list(bin_value[2:])]
        bin_value = ([0] * (args_num - len(bin_value))) + bin_value
        mask.append(bin_value)

    return mask


# solves the expression for the given bit mask


def solve_for_mask(mask, rpn_expr, variables):

    stack = []

    for char in rpn_expr:

        if char in variables:
            stack.append(mask[variables.index(char)])

        if char in "01":
            stack.append(int(char))

        if char == "|":
            a = stack.pop()
            b = stack.pop()
            stack.append((a or b))

        if char == "&":
            a = stack.pop()
            b = stack.pop()
            stack.append((a and b))

        if char == "^":
            a = stack.pop()
            b = stack.pop()
            stack.append(a ^ b)

        if char == "~":
            a = stack.pop()
            stack.append(not a)

        if char == ">":
            a = stack.pop()
            b = stack.pop()
            stack.append((not a) or b)

        if char == "=":
            a = stack.pop()
            b = stack.pop()
            stack.append(a == b)

    return stack.pop()


# compares two bit masks


def compare(a, b):

    res = []
    count = 0

    for i in range(len(a)):

        if a[i] == b[i]:
            res.append(a[i])
        else:
            res.append('-')
            count += 1

    if count > 1:       # bit masks can differ by one
        return None

    return res


def reduce(values, const):

    length = len(values)
    to_change = []
    used = [0] * length

    for i in range(length):
        for j in range(i+1, length):

            res = compare(values[i], values[j])

            if res is not None:
                to_change.append(res)
                used[i] = 1
                used[j] = 1

    # if masks where not used then they will not be reduced anymore
    const += [x for x in values if used[values.index(x)] == 0]

    # if there is only one digit left then masks will not be reduced anymore
    for i in to_change:
        if len([x for x in i if x != '-']) == 1:
            const.append(i)

    to_change = [x for x in to_change if x not in const]

    return [to_change, const]


# checks if the value is in the given reduced bit mask


def is_in_result(reduced, val):

    for i in range(len(val)):

        if (val[i] != reduced[i]) and (reduced[i] != '-'):
            return False

    return True


def quine_mccluskey(rpn_expr, variables):

    if not variables:
        return solve_for_mask({}, rpn_expr, variables)

    mask = create_mask(len(variables))      # all possible bit combinations
    new_mask = []                           # bit masks for which the result is 1

    for i in range(len(mask)):

        j = solve_for_mask(mask[i], rpn_expr, variables)
        if j == 1:
            new_mask.append(mask[i])

    if not new_mask:
        return 0

    const = []
    values = new_mask

    while values:
        [values, const] = reduce(values, const)          # minimize the masks

    used = {}

    # create the dictionary keys which are reduced masks
    for i in range(len(const)):
        used["".join(str(x) for x in const[i])] = set()

    # add values - not reduced bit masks to the keys
    for i in range(len(new_mask)):
        for j in const:
            if is_in_result(j, new_mask[i]):
                used["".join(str(x) for x in j)].add("".join(str(x) for x in new_mask[i]))

    res = []

    while used:

        # find the keys for which the number of masks is minimal
        min_value = min(len(x) for x in list(used.values()))
        min_key = list(x for x in used.keys() if len(used[x]) == min_value)

        while min_key:

            key = min_key.pop()
            tmp_values = list(used[key])

            # removes all values in the dictionary which are in tmp_values
            for i in list(used.keys()):
                used[i] = {x for x in list(used[i]) if x not in tmp_values}

            res.append(key)
            del used[key]

            # remove all keys which do not have sets anymore
            for i in list(used.keys()):
                if len(used[i]) == 0:
                    del used[i]

            if not used:
                break

    return res


# converts the result of the algorithm to one expression with the proper variables names


def to_string(res, variables):

    reduced = ""

    for i in res:
        for j in range(len(i)):

            if i[j] == '1':
                reduced += variables[j]
            elif i[j] == '0':
                reduced += ('~' + variables[j])

        if res.index(i) != (len(res) - 1):
            reduced += " + "

    return reduced


if __name__ == '__main__':

    print("Please type the expression: ")
    expression = input()
    [new_expression, arguments] = validate(expression)

    if new_expression:

        rpn_expression = to_rpn(new_expression, arguments)

        if '1' in arguments:
            arguments.remove('1')
        if '0' in arguments:
            arguments.remove('0')

        arguments = list(arguments)
        result = quine_mccluskey(rpn_expression, arguments)

        if isinstance(result, list):
            print(to_string(result, arguments))
        else:
            print(result)
