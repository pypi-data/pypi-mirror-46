import sys
def print_lol(list_1, indent=False, other=0, position=sys.stdout):
    for each in list_1:
        if isinstance(each, list):
            print_lol(each, indent, other+1, position)
        else:
            if indent:
                for tab in range(other):
                    print("\t", end="", file = position)
            print(each, file = position)