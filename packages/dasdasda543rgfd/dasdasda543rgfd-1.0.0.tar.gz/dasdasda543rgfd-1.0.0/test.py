def print_lol(list_1):
    for each in list_1:
        if isinstance(list_1, list):
            print_lol(each)
        else:
            print(each)