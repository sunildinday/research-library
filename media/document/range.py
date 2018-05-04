def ranges(start, end, steps):
    ans = []
    print steps
    temp = start
    for value in range(start, end):
        ans.append(temp)
        temp = temp + steps
        print temp
        if temp > end:
            break
    return ans
print ranges(5, 40, 6)
