"""This is a python comment"""
#this is another comment
def print_lol(the_list):
    """This is another python comment"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)