def prt_vec (v: list, desc: str='#'*50, dec: int=3) -> None:
    if v:
        print(desc)
        print([round(vi, dec) for vi in v])
        print(desc)
    else:
        print('Not a vector')


def prt_mat(m: list, desc: str='#'*50, rnd: bool=False, dec: int=3) -> None:
    if m:
        print(desc)
        for row in m:
            if rnd:
                print(*[round(el, dec) for el in row])
            else:
                print(*row)
        print(desc)
    else:
        print('Not a matrix')

def matmul(m1: list, m2: list):

    nrows = len(m1)
    ncols = len(m2[0])
    mult = [[0] * ncols for i in range(nrows)]

    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                mult[i][j] += m1[i][k] * m2[k][j]
       
    return mult


def transpose(m) -> list:
    return map(list, zip(*m))


def separate(m: list, col_num: int) -> list:
    nrows = len(m)
    cols = len(m[0])
    ncols1 = col_num
    ncols2 = cols - col_num

    m1 = [[0] * ncols1 for row in range(nrows)]
    m2 = [[0] * ncols2 for row in range(nrows)]

    for row in range(nrows):
        for col in range(cols):
            if (col < col_num):
                m1[row][col] = m[row][col]
            else:
                m2[row][col - col_num] = m[row][col]

    return [m1, m2]


def is_square(m) -> bool:
    if not (len(m) == len(m[0])):
        return False
    else:
        return True


def swap_row(m: list, i: int, j: int) -> list:
    temp = [el for el in m[i]]
    m[i] = m[j]
    m[j] = temp
    return m


def join(m1, m2) -> list:
    return [[*row1, *row2] for row1, row2 in zip(m1, m2)]


def find_row_with_max_element(m, col_num: int=0, starting_row: int=0):
    tmp = m[starting_row][col_num]
    row_idx = starting_row
    for k in range(starting_row+1, len(m)):
        if abs(m[k][col_num]) > abs(tmp):
            row_idx = k
            tmp = m[k][col_num]
    return row_idx


def identity(ndim: int) -> list:
    
    matrix = [[0] * ndim for row in range(ndim)]

    for i in range(len(matrix)):
        matrix[i] = [1 if i == j else 0 for j in range(len(matrix))]
    
    return matrix


def compare(m1: list, m2: list) -> bool:
    
    if not (len(m1) - len(m2)) or not (len(m1[0]) - len(m2[0])):
        return False
        
    for m1_row, m2_row in zip(m1, m2):
        for el_1, el_2 in zip(m1_row, m2_row):
            if (el_1 - el_2) > 10 ** -6:
                return False

    return True

def inverse(m) -> list:
    if not is_square(m):
        return False

    identity_matrix = identity(ndim=len(m))
    num_rows = len(m) - 1
    joint_matrix = join(m, identity_matrix)

    flag = False
    count = 0
    max_count = 100

    while not flag and count < max_count:
        for i in range(num_rows + 1):
            if joint_matrix[i][i] == 0.0:
                max_el_idx = find_row_with_max_element(joint_matrix, i, i)
                joint_matrix = swap_row(joint_matrix, i, max_el_idx)
            div_e = joint_matrix[i][i]
            factor = 1 / div_e
            joint_matrix[i] = [e * factor for e in joint_matrix[i]]
            for row in range(0, num_rows+1):
                if row != i:
                    if joint_matrix[row][i] != 0:
                        sub = (-1) * joint_matrix[row][i]
                        row_add = [el * sub for el in joint_matrix[i]]
                        joint_matrix[row] = [e1 + e2 for e1, e2 in zip(row_add, joint_matrix[row])]
    
        identity_matrix, inverse_matrix = separate(m=joint_matrix, col_num=num_rows+1)
        if not compare(identity(ndim=num_rows+1), identity_matrix):
            flag = True
        count += 1
    
    if not flag:
        return False
    else:
        return inverse_matrix
