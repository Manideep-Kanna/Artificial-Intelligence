def min_value(arr):
    min_num = arr[0]
    for num in arr:
        if num < min_num:
            min_num = num
            
    return min_num

print(min_value([78,3,1,90,-1]))