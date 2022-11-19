
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
                total_groups += 1
                break
    
    return total_groups


def group_processor(groupstr):
    total_value = ''
    len_groups = 0
    
    for i in range(0, len(groupstr), 5):
        group_start = i + 1
        group_indexes = i + 5
        value = groupstr[group_start: group_indexes]
        total_value += value
        len_groups += 1

        if groupstr[i] == '0':
            return bintodec(total_value), len_groups


def runner(proc_str: str):
    version_sum = 0
    stack = []
    running = True

    while running:
        # stack node updater
        if len(stack) != 0 and stack[-1]["processed"] == stack[-1]["count"]:
            done_node = stack.pop()

            # stop if stack has reached zero
            if len(stack) == 0:
                break

            # TODO process subpackets according to type_id (packet_value)
            # TODO update/add to parent subpack_values

            # update parent continue
            stack[-1]["total_bits"] += done_node["total_bits"]
            if stack[-1]["type"] == "bits":
                stack[-1]["processed"] += done_node["total_bits"]
            else:
                stack[-1]["processed"] += 1  # subpack
            
            continue

        packet_version = bintodec(proc_str[:3])
        type_version = bintodec(proc_str[3:6])

        # if literal
        if type_version == 4:
            #len_groups = group_counter(proc_str[6:])
            # TODO get actual packet value
            packet_value, len_groups = group_processor(proc_str[6:])
            package_bits = 6 + (len_groups * 5)  # TODO process forreal
            version_sum += packet_version

            # update parent node processes
            if stack[-1]["type"] == "bits":
                stack[-1]["processed"] += package_bits
            else:
                stack[-1]["processed"] += 1  # subpacks

            # update bits count
            stack[-1]["total_bits"] += package_bits

            # update subpacket values
            stack[-1]["subpack_values"].append(packet_value)
            
            # return remaining proc
            proc_str = proc_str[package_bits:]
            continue
            
        # operator processing section
        length_type = proc_str[6]

        if length_type == '0':
            # operator_type 0 flow
            bits = bintodec(proc_str[7:22])
            version_sum += packet_version
            stack.append({
                "type": "bits",
                "count": bits,
                "processed": 0,
                "total_bits": 22,
                "type_version": type_version,
                "subpack_values": []
                # TODO subpacket_values, type_id

            })

            # return remaining
            proc_str = proc_str[22:]
            continue
        else:
            # operator_type 1 flow
            subpacks = bintodec(proc_str[7:18])
            version_sum += packet_version
            stack.append({
                "type": "subpacks",
                "count": subpacks,
                "processed": 0,
                "total_bits": 18,
                "type_version": type_version,
                "subpack_values": []
                # TODO subpacket_values, type_id
            })

            # return remaining
            proc_str = proc_str[18:]
            continue

    return version_sum
    

if __name__ == '__main__':
    ex1 = hextobin('8A004A801A8002F478')
    ex2 = hextobin('620080001611562C8802118E34')
    ex3 = hextobin('C0015000016115A2E0802F182340')
    ex4 = hextobin('A0016C880162017C3686B18A3D4780')
    real = hextobin('4057231006FF2D2E1AD8025275E4EB45A9ED518E5F1AB4363C60084953FB09E008725772E8ECAC312F0C18025400D34F732333DCC8FCEDF7CFE504802B4B00426E1A129B86846441840193007E3041483E4008541F8490D4C01A89B0DE17280472FE937C8E6ECD2F0D63B0379AC72FF8CBC9CC01F4CCBE49777098D4169DE4BF2869DE6DACC015F005C401989D0423F0002111723AC289DED3E64401004B084F074BBECE829803D3A0D3AD51BD001D586B2BEAFFE0F1CC80267F005E54D254C272950F00119264DA7E9A3E9FE6BB2C564F5376A49625534C01B0004222B41D8A80008446A8990880010A83518A12B01A48C0639A0178060059801C404F990128AE007801002803AB1801A0030A280184026AA8014C01C9B005CE0011AB00304800694BE2612E00A45C97CC3C7C4020A600433253F696A7E74B54DE46F395EC5E2009C9FF91689D6F3005AC0119AF4698E4E2713B2609C7E92F57D2CB1CE0600063925CFE736DE04625CC6A2B71050055793B4679F08CA725CDCA1F4792CCB566494D8F4C69808010494499E469C289BA7B9E2720152EC0130004320FC1D8420008647E8230726FDFED6E6A401564EBA6002FD3417350D7C28400C8C8600A5003EB22413BED673AB8EC95ED0CE5D480285C00372755E11CCFB164920070B40118DB1AE5901C0199DCD8D616CFA89009BF600880021304E0EC52100623A4648AB33EB51BCC017C0040E490A490A532F86016CA064E2B4939CEABC99F9009632FDE3AE00660200D4398CD120401F8C70DE2DB004A9296C662750663EC89C1006AF34B9A00BCFDBB4BBFCB5FBFF98980273B5BD37FCC4DF00354100762EC258C6000854158750A2072001F9338AC05A1E800535230DDE318597E61567D88C013A00C2A63D5843D80A958FBBBF5F46F2947F952D7003E5E1AC4A854400404A069802B25618E008667B7BAFEF24A9DD024F72DBAAFCB312002A9336C20CE84')
    version_sum = runner(real)

    print(version_sum)

