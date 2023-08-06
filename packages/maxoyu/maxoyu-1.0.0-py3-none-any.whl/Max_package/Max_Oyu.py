def find_max(my_list):
    ikh = my_list[0]
    for e in my_list:
        if ikh < e:
            ikh = e
    return ikh


if __name__ == "__main__":
    print(find_max([1, 2, 3, 4, 5]))


# list_m = [1, 2, 3, 4, 5, 6]
# print(find_max(list_m))
# print(max(list_m))

# def find_max(my_list):
#     ikh = my_list[0]
#     i = len(my_list)
#     j = 0
#     while j < i:
#         if ikh > my_list[j]:
#             print(ikh)
#         j += 1


# find_max([1, 2, 3, 4])


# def tomruulakh(utga):
#     print(utga.upper())
