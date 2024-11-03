count = 18
prev_2 = 0
prev_1 = 1

print(prev_2)
print(prev_1)

def fibonacii(prev_1,prev_2):
    global count
    if count <=0:
        return
    new_fibo = prev_1 + prev_2
    print(new_fibo)
    count -=1
    fibonacii(new_fibo,prev_1)

fibonacii(prev_1,prev_2)