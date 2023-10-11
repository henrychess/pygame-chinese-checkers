def func(num):
    num += 1
    print(f"num: {num}")
    if num % 2 == 0 and num < 10:
        func(num)
    return num

num = 1
for i in range(2):
    num += func(num)
    print(num)
print(f"fin: {num}")