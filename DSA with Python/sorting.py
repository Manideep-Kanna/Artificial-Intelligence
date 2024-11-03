def swap(arr,i,j):
    arr[i],arr[j] = arr[j],arr[i]
    
def bubble_sorting(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if (arr[j] > arr[j+1]):
                swap(arr,j,j+1)
    print(arr)
    
def insertion_sort(arr):
    n = len(arr)
    for i in range(1,n):
        ind = i
        curr_val = arr[i]
        for j in range(i-1,-1,-1):
            if arr[j] > curr_val:
                arr[j+1] = arr[j]
                ind = j
            else:
                break
        arr[ind] = curr_val
    print(arr)
    
def quick_sort(arr,low,high):
    if low >= high:
        return
    i = low
    j = high 
    pivot = low
    while i<=j:
        while i<= high and arr[i] <= arr[pivot]:
            i+=1
        while j>= low and arr[j] > arr[pivot]:
            j-=1
        if i<=j:
            arr[i],arr[j] = arr[j],arr[i]
    arr[pivot],arr[j] = arr[j],arr[pivot]
    partition_ind = j
    quick_sort(arr,low,partition_ind-1)
    quick_sort(arr,partition_ind+1,high)

def count_sort(arr):
    max_len = max(arr)
    count_arr = [0]* (max_len + 1)
    new_arr=[]
    for i in arr:
        count_arr[i]+=1
    for i in range(len(count_arr)):
        while(count_arr[i] >0):
            new_arr.append(i)
            count_arr[i]-=1
    print(new_arr)
    
def radix_sort(arr):
    divisor = 1
    max_num = max(arr)
    k = len(str(max_num))
    
    while(k > 0):
        radix_arr = [[] for _ in range(10)]
        for i in range(len(arr)):
            num = arr[i]
            num /= divisor
            digit = int(num %10)
            radix_arr[digit].append(arr[i])
        arr.clear()
        for digit_arr in radix_arr:
            print("Came here")
            for number in digit_arr:
                arr.append(number)
        radix_arr.clear()
        
        
        divisor *=10    
        k-=1
    print(arr)
    
def merge(arr,low,mid,high):
    temp = []
    i = low
    j = mid+1
    k = low
    while i<=mid and j<=high:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i+=1
        else:
            temp.append(arr[j])
            j+=1
    while i<=mid:
        temp.append(arr[i])
        i+=1
    while j<=high:
        temp.append(arr[j])
        j+=1

    for i in range(low,high+1):
        arr[i] = temp[i-low]
    

def merge_sort(arr,low,high):
    if low>=high:
        return 
    mid = (low+high) // 2
    
    merge_sort(arr,low,mid)
    merge_sort(arr,mid+1,high)
    
    merge(arr,low,mid,high)
    
      

# bubble_sorting([43,1,3,56,78,98])
# insertion_sort([43,1,3,56,78,98])
# count_sort([9,5,6,7,2,3,1,5,6,8,9])
# radix_sort([170, 45, 75, 90, 802, 24, 2, 66])

# arr = [8,7,9,2,3,6,1,0]
# quick_sort(arr,0,len(arr)-1)
# print(arr)

arr1 = [3,1,2,4,1,5,6,2]
merge_sort(arr1,0,len(arr1) -1)
print(arr1)


