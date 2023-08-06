def find_max (my_list):
    max = my_list [0]
    for e in my_list:
        if max < e:
            max = e
    return max

my_list = ([1, 30, 100, 23, 2])
print (find_max(my_list))