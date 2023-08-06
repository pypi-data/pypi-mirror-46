"""
This is the “nester.py" module, and it provides one function called print_list() which prints
lists that may or may not include nested lists.
"""


def print_list(list_items):
    """
    This function takes a list and prints all the elements even if there are
    nested list one after the other
    :param list_items:
    :return:
    """
    for item in list_items:
        if isinstance(item, list):
            print_list(item)
        else:
            print(item)