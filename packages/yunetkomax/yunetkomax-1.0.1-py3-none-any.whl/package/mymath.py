def find_max (my_list):
    max = my_list [0]
    for e in my_list:
        if max < e:
            max = e
    return max

if __name__ == "__main__":
print(find_max([1, 10, 30,150,2]))