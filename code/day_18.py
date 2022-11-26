

def dissect(nodes, level = []):
    left_node = nodes[0]
    right_node = nodes[1]
    depth = len(level)

    if type(left_node) is int:
        print('end L', left_node, level + [0])
        return level
    else:
        if (depth + 1) == 4:
            print('explosion!')
            return level
        print(left_node, level + [0])
        dissect(left_node, level + [0])

    if type(right_node) is int:
        print('end R', right_node, level + [1])
        return level
    else:
        if (depth + 1) == 4:
            print('explosion')
            return level
        dissect(right_node, level + [1])
        #print('dissect', right_node, level + [1])


test_nodes = [[[[[4,3],4],4],[7,[[8,4],9]]], [1, 1]]

result = dissect(test_nodes)

print('done')