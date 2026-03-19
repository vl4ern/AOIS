def binary_cum(bits_1: list, bits_2: list[int]) -> list[int]:
    result = []
    ratio = 0

    if len(bits_1) > len(bits_2):
        for i in range(len(bits_1) - 1, -1, -1):
            total = bits_1[i] + bits_2[i] + ratio
            result.append(total % 2)
            ratio = total // 2

        if ratio < 0:
            return result
        
    else:
        for i in range(len(bits_2) - 1, -1, -1):
            total = bits_2[i] + bits_1[i] + ratio
            result.append(total % 2)
            ratio = total // 2

        if ratio < 0:
            return result