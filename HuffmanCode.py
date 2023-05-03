import heapq
import unidecode

# Function that removes accents
def remove_accents(text):
    return unidecode.unidecode(text)

# Function that creates the frequency table based in the message
def create_probability_table(message):
    frequency = {}
    for char in message:
        if char in frequency:
            frequency[char] += 1  # case key exit
        else:
            frequency[char] = 1  # case key does not exist
    return frequency


# Function thta creates the huffman codification as dictionary
def huffman_code_tree(freq):
    heap = [[wt, [sym, ""]] for sym, wt in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))


# Encode function
def encode(message, code):
    encoded_message = ""
    for char in message:
        encoded_message += code[char]
    return encoded_message


# Decode function
def decode(encoded_message, huffman_Code):
    reverse_mapping = {v: k for k, v in huffman_Code.items()}
    decoded_message = ""
    i = 0
    while i < len(encoded_message):
        code = ""
        while (code not in reverse_mapping) and (i < len(encoded_message)):
            code += encoded_message[i]
            i += 1
        if code in reverse_mapping:
            decoded_message += reverse_mapping[code]
    return decoded_message


def main():
    # Open file and read message
    with open('input.txt', 'r') as f:
        string = f.read()
    # string = input()

    # Remove accents from message
    string = remove_accents(string)

    freq = create_probability_table(string)
    huffman_code = huffman_code_tree(freq)
    print(' Char | Huffman code ')
    print('----------------------')
    for (char, frequency) in freq.items():
        print(' %-4r |%12s' % (char, huffman_code[char]))

    # Encodes the message
    sencode: str = encode(string, huffman_code)
    print(sencode)

    # Decodes the message
    sdecode: str = decode(sencode, huffman_code)
    print(sdecode)

    # Write decoded message to file
    with open('decoded_message.txt', 'w') as f:
        f.write(sdecode)


if __name__ == '__main__':
    main()
