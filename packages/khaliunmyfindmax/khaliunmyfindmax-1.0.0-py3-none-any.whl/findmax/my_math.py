def find_max(my_list):
    max = my_list[0]
    for e in my_list:
        if e > max:
            max = e
    return max


# print(find_max(list_m))

# if __name__ == "__main__":
print(find_max([11, 2, 3, 4, 5, 6]))
