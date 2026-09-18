import numpy as np

def mult_shift(x, k):
    #x: input block
    #k: -1 or shift
    #y: output

    if (k == -1):
        y = np.zeros(len(x), dtype=int)
    else:
        y = np.concatenate((x[k:], x[:k]))
    return y

def check_cword(base_matrix, z, cword):
    #z: expansion factor
    
    m, n = base_matrix.shape

    syn = np.zeros(m*z, dtype=int) #Hc^T

    for i in range(m):
        for j in range(n):
            syn[i*z:(i+1)*z] = syn[i*z:(i+1)*z] ^ mult_shift(cword[j*z:(j+1)*z], base_matrix[i,j])

    return False if np.any(syn) else True

def nr_ldpc_encode(base_matrix, z, msg):
    #z: expansion factor
    #msg: message
    
    m, n = base_matrix.shape

    cword = np.zeros(n*z, dtype=int)
    cword[0:(n-m)*z] = msg

    #double diagonal encoding
    temp = np.zeros(z, dtype=int)
    for i in range(4): #row 0 to 3
        for j in range(n-m): #message columns
            temp = temp ^ mult_shift(msg[j*z:(j+1)*z], base_matrix[i,j])
    if base_matrix[1,n-m] == -1:
        p1_sh = base_matrix[2,n-m]
    else:
        p1_sh = base_matrix[1, n-m]
    cword[(n-m)*z:(n-m+1)*z] = mult_shift(temp,z-p1_sh) #p1

    #find p2,p3,p4
    for i in range(3):
        temp = np.zeros(z, dtype=int)
        for j in range(n-m+i+1):
            temp = temp ^ mult_shift(cword[j*z:(j+1)*z], base_matrix[i,j])
        cword[(n-m+i+1)*z:(n-m+i+2)*z] = temp

    #remaining parties
    for i in range(4, m):
        temp = np.zeros(z, dtype=int)
        for j in range(n-m+4):
            temp = temp ^ mult_shift(cword[j*z:(j+1)*z], base_matrix[i,j])
        cword[(n-m+i)*z:(n-m+i+1)*z] = temp

    return cword