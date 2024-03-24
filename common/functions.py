
def compress(categories):
    w = len(categories)
    if w > 0:
        h = len(categories[0])
        if h > 0:
            compressed_size = 2 + int((w * h) / 8) + (1 if (w * h) % 8 > 0 else 0)
            compressed_bytes = bytearray(compressed_size)
            compressed_bytes[0] = w
            compressed_bytes[1] = h

            count = 0
            value = 0
            index = 2
            for i in range(0, w):
                for j in range(0, h):
                    b = categories[i][j]
                    value = (value << 1) + (b & 0x01)
                    count += 1
                    if count == 8:
                        compressed_bytes[index] = value
                        index += 1
                        count = 0
                        value = 0
            if count > 0:
                value = value << (8 - count)
                compressed_bytes[index] = value
            return compressed_bytes
    return []

def decompress(data):
    l = len(data)

    categories = []
    if l <= 2:
        return categories

    w = data[0]
    h = data[1]

    index = 2
    value = data[index]
    index += 1
    count = 0
    for i in range(0, w):
        barray = [0] * h
        for j in range(0, h):
            barray[j] = (value >> (7 - count)) & 0x01
            count += 1
            if count == 8:
                value = data[index]
                index += 1
                count = 0
        categories.append(barray)

    return categories


def count_changed_bits(byte1, byte2):
    # XOR the two bytes to find differing bits
    xor_result = byte1 ^ byte2
    # Count the number of set bits (1s) in the XOR result
    changed_bits_count = bin(xor_result).count('1')
    return changed_bits_count

def change_detection(old, new, threshold=10):
    l_old = len(old)
    l_new = len(new)

    if l_old != l_new:
        return True

    w_old = old[0]
    w_new = new[0]
    if w_old != w_new:
        return True

    h_old = old[1]
    h_new = new[1]
    if h_old != h_new:
        return True

    change_count = 0
    total_count = w_new * h_new
    for i in range(2, l_new):
        change_count += count_changed_bits(old[i], new[i])

    return (change_count / total_count) > (threshold / 100)


if __name__ == "__main__":
    cate = [
        [1, 0, 1],
        [0, 1, 1],
        [0, 0, 0]
    ]

    bytes = compress(cate)
    print(bytes)

    new_cate = decompress(bytes)
    print(new_cate)

    cate2 = [
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
    ]

    bytes2 = compress(cate2)
    print(bytes2)

    new_cate2 = decompress(bytes2)
    print(new_cate2)

    cate3 = [
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
    ]

    bytes3 = compress(cate3)
    print(bytes3)

    print(change_detection(bytes2, bytes3))
