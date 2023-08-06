
def list_replace(the_list, item, replacement):
    new = the_list.copy()
    for i in range(len(new)):
        if new[i] == item:
            new[i] = replacement
    return new