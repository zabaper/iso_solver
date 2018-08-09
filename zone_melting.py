'''
Author: iaiaoee

Contributors:

Math proof:
-

Algorithm:
-

Algorithm implementation:
-

'''

import operator


def build_destination_map(matrix, size):
    last_index = size + 1

    current_level = 1
    for position_y, line in enumerate(matrix):
        line[position_y] = 0

    is_find = True

    while is_find:
        is_find = False

        for position_y, line in enumerate(matrix):

            if line[last_index] == 1:
                continue

            line_stack = []
            level_stack = []

            for position_x, item in enumerate(line):
                if position_x == size:
                    break

                if item == 0 and position_x != position_y:
                    line_stack.append(position_x)

                if item == current_level:
                    level_stack.append(position_x)

            if not line_stack:
                line[last_index] = 1
            else:
                for position_x in level_stack:
                    for position_xx in line_stack:
                        if matrix[position_x][position_xx] == 1:
                            is_find = True
                            matrix[position_y][position_xx] = current_level + 1
                            matrix[position_xx][position_y] = current_level + 1

        current_level = current_level + 1


def build_index(matrix, zone_level, matrix_len, max_item):
    stop = matrix_len - 1
    for i in range(zone_level, stop):
        line = matrix[i]

        line[matrix_len] = '-'.join(str(line[i]) for i in range(zone_level))
        line[matrix_len] += '|'
        line[matrix_len] += '-'.join(str(line[zone_level:stop].count(i)) for i in range(max_item))


def get_index(matrix, zone_level, matrx_size):
    s1 = matrx_size + 1
    s2 = matrx_size + 2

    complex_index = []
    index = []
    for i in range(zone_level, matrx_size):
        index.append(matrix[i][s1])
        complex_index.append(matrix[i][matrx_size:s2] + [''])

    for line in complex_index:
        line[2] = index.count(line[1])

    complex_index.sort(key=operator.itemgetter(2, 1))
    index.sort()

    return complex_index, index


def swap(matrix, i, j):
    matrix[i], matrix[j] = matrix[j], matrix[i]
    for item in matrix:
        item[i], item[j] = item[j], item[i]


def sort_matrix(matrix, index, zone_level, level_gap, matrix_size):
    for i in range(level_gap):
        if matrix[i+zone_level][matrix_size] == index[i][0]:
            continue

        for j in range(i + zone_level + 1, matrix_size):

            if matrix[j][matrix_size] == index[i][0]:
                swap(matrix, i + zone_level, j)
                break


def sort_matrix_1(left, right, zone_level, level_gap, index, matrix_size):
    index_count = 0

    l1 = zone_level + 1

    for i in range(zone_level, matrix_size):
        if left[i][matrix_size+1] == index:
            if i != zone_level:
                swap(left,i,zone_level)
            break

    for i in range(zone_level,matrix_size):
        if index_count  == level_gap:
            break

        if right[i][matrix_size+1] == index:
            index_count += 1

            if i != zone_level:
                swap(right,i,zone_level)

            if left[zone_level][:l1] == right[zone_level][:l1]:
                return False

        

    return True


def refine(a, b):
    iteration = 0
    len_a1 = len(a)
    len_a2 = len(a[0])

    if len_a2 != len_a1 + 1:
        return [], 'Wrong matrix a'

    len_b1 = len(b)
    len_b2 = len(b[0])

    if len_b2 != len_b1 + 1:
        return [], 'Wrong matrix b'

    if len_a1 != len_b1:
        return [], 'Isomorphism impossible'

    matrix_size = len_a1

    left = [line + [''] for line in a]
    right = [line + [''] for line in b]

    zone_level = 0

    build_destination_map(left, matrix_size)
    build_destination_map(right, matrix_size)

    max_left = max(line[i] for line in left for i in range(matrix_size))
    max_right = max(line[i] for line in right for i in range(matrix_size))

    max_both = max(max_left, max_right)
    max_both += 1

    while zone_level < matrix_size:

        iteration += 1

        build_index(left, zone_level, len_a2, max_both)
        build_index(right, zone_level, len_a2, max_both)

        ci_l, i_l = get_index(left, zone_level, matrix_size)
        ci_r, i_r = get_index(right, zone_level, matrix_size)

        if i_l != i_r:
            return [], 'Isomorphism impossible matrix size:{} iteration:{}'.format(matrix_size,iteration)

        min_index = ci_l[0][2]



        if min_index == 1:

            level_gap_i = [line[2] for line in ci_l]
            level_gap = level_gap_i.count(min_index)

            sort_matrix(left, ci_l, zone_level, level_gap, matrix_size)
            sort_matrix(right, ci_r, zone_level, level_gap, matrix_size)

        else:
            not_ok = sort_matrix_1(left, right, zone_level, min_index,ci_l[0][1],matrix_size)

            if not_ok:
                return [], 'Isomorphism impossible matrix size:{} iteration:{}'.format(matrix_size,iteration)

            level_gap = 1

        zone_level += level_gap

    t_l = [line[:matrix_size] for line in left]
    t_r = [line[:matrix_size] for line in right]

    if t_l != t_r:
        return [], 'Isomorphism impossible matrix size:{} iteration:{}'.format(matrix_size,iteration)

    ret = [[left[i][matrix_size]] + [right[i][matrix_size]] for i in range(matrix_size)]
    return ret, 'matrix size:{} iteration:{}'.format(matrix_size,iteration)
