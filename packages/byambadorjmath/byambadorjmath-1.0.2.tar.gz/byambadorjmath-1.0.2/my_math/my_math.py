
def find_max(my_list):
    ikh = my_list[0]
    for element in my_list:
        if ikh < element:
            ikh = element
    return ikh


# print(find_max([1, 30, 100, 23, 2]))
