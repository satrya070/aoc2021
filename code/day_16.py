
hexmap = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

def bintodec(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal


def hextobin(hexstring):    
    binstring = ''
    for c in hexstring:
        binstring += hexmap[c]
    
    return binstring


def group_counter(groups):
    total_groups = 1
    
    if groups[0] == '0':
        return total_groups

    for k, i in enumerate(groups):
        if (k+1) % 5 == 0:
            if groups[k+1] == '1':
                total_groups += 1
            else:
                break
    
    return total_groups


def recur2(proc_str, subpacks=None):
    packet_version = bintodec(proc_str[:3])
    type_version = bintodec(proc_str[3:6])
    
    if type_version != 4:
        # operator
        length_type = proc_str[6]

        if length_type == '0':
            # 15 bits version flow
            subbits = bintodec(proc_str[7:22])
            print(packet_version, type_version, length_type, subbits)
            return recur(proc_str[22:22+subbits])
        else:
            # 11-bit subpack flow
            subpacks = bintodec(proc_str[7:18])
            print(packet_version, type_version, length_type, subpacks)
            for i in range(subpacks):
                proc_str = recur(proc_str[18:])
            
            return recur(proc_str[18:], subpacks)
    else:
        # literal (end_node)
        print(packet_version, type_version, 'end')
        # count groups * 5
        len_groups = group_counter(proc_str[5:])
        # subpacks -= 1
        literal_length = 6 + len_groups * 5
        return recur(proc_str[literal_length:], subpacks)


def recur(proc_str: str, stype: str=None, subbits: int=0):
    packet_version = bintodec(proc_str[:3])
    type_version = bintodec(proc_str[3:6])

    # handle literal handle and return
    if type_version == 4:
        len_groups = group_counter(proc_str[6:])
        package_bits = 6 + (len_groups * 5)
        if stype == 'b':
            return package_bits
        else:  # s
            return 1 # in while loop?

    # operator flow
    length_type = proc_str[6]
    if length_type == '0':
        # operator-0 flow
        bits = bintodec(proc_str[7:22])
        processed_bits = 0

        while processed_bits != bits:
            recur(proc_str[22:], 'bits', bits)

    else:
        # operator-1 flow
        subpacks = bintodec(proc_str[7:18])
        return recur(proc_str[18:], 'subs', subpacks)


def runner(proc_str: str):
    stack = []
    running = True

    while running:
        # if stack[-1]["processed"] == stack[-1]["count"]:
        # pop it
        # update parent continue

        packet_version = bintodec(proc_str[:3])
        type_version = bintodec(proc_str[3:6])

        # if literal
        if type_version == 4:
            len_groups = group_counter(proc_str[6:])
            package_bits = 6 + (len_groups * 5)

            # update current node process
            if stack[-1]["type"] == "bits":
                stack[-1]["processed"] += package_bits
            else:
                stack[-1]["processed"] += 1  # subpacks

            # update bits count
            stack[-1]["total_bits"] += package_bits

            # current node processing is done
            if stack[-1]["processed"] == stack[-1]["count"]:
                done = stack.pop()

                # update parent when child is finished
                if stack[-1]["type"] == "bits":
                    stack[-1]["processed"] += done["total_bits"]
                else:
                    stack[-1]["processed"] += 1  # subpacks
                
                # update parent total bits
                stack[-1]["total_bits"] += done
            
            # return remaining proc
            proc_str = proc_str[package_bits:]
            continue

        # operator processing section
        length_type = proc_str[6]

        if length_type == '0':
            # operator_type 0 flow
            bits = bintodec(proc_str[7:22])
            stack.append({
                "type": "bits",
                "count": bits,
                "processed": 0,
                "total_bits": 22
            })

            # return remaining
            proc_str = proc_str[22:]
            continue
        else:
            # operator_type 1 flow
            subpacks = bintodec(proc_str[7:18])
            stack.append({
                "type": "subpacks",
                "count": subpacks,
                "processed": 0,
                "total_bits": 18
            })

            # return remaining
            proc_str = proc_str[18:]
            continue
    

if __name__ == '__main__':
    ex2 = hextobin('620080001611562C8802118E34')
    runner(ex2)

