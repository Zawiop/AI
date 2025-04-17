def handleVscle(vslc, size, width):
    arr = range(0,size)
    colonCount = vslc.count(':')
    if '#' in vslc:
        nums = vslc.split('#')
        end = []
        if nums[0] == '': nums[0] = 0
        if nums[1] == '': nums[1] = size-1

        for r in range(int(nums[0]), int(nums[1]), width):
            for val in range(r, r+(int(nums[1]) % width) + 1):
                end.append(arr[val])
        return end
    
    elif colonCount == 0:
        return [arr[int(vslc)]]
    
    elif colonCount == 1:
        nums = vslc.split(':')

        for idx, x in enumerate(nums):
            if x == '':
                nums[idx] = None

        return arr[int(nums[0]): int(nums[1])]
    else:

        nums = vslc.split(':')
        for idx, x in enumerate(nums):
            if x == '':
                nums[idx] = None
        # work on middle num

        if not nums[1]: nums[1] = size
        if not nums[2]: nums[2] = 1
        return [*arr[int(nums[0]) : int(nums[1]) : int(nums[2])]]

print(handleVscle('2::4', 12, 4))