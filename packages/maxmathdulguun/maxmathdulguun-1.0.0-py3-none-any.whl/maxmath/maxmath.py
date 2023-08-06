def find_max(my_list):
    max_number = my_list[0]
    for number in my_list:
        if number > max_number:
            max_number = number
    return max_number

if __name__ == "__main__":
    my_list = [1, 2, 3, 101, 24]
    maxlist = find_max(my_list)
    print(maxlist)
