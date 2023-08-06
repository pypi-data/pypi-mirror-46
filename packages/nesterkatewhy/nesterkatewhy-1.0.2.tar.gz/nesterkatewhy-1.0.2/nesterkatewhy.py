""" This is the nester.py module that provides a function. This function can print the item of a list."""

def print_lol(data, indent=False, level=0):
    for item in data:
        if isinstance(item, list):
            print_lol(item, indent, level+1)
        else:
            if indent:
                for i in range(level):
                    print("\t", end='')
            print(item)

