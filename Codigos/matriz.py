import numpy as np

def reorganizar_bg(matriz_original):
    M, N = matriz_original.shape

    # Identifica se é BG1 (46x68) ou BG2 (42x52) pelas dimensões
    if M == 46 and N == 68:  # BG1
        c_a, c_e, c_o = 22, 4, 42
        r_topo, r_base = 4, 42
    elif M == 42 and N == 52:  # BG2
        c_a, c_e, c_o = 10, 4, 38
        r_topo, r_base = 4, 38
    else:
        raise ValueError(f"Dimensão {M}x{N} não corresponde a BG1 nem BG2.")

    # 1. Fatiamento dos 6 blocos originais
    A = matriz_original[0:r_topo, 0:c_a]
    E = matriz_original[0:r_topo, c_a : c_a + c_e]
    O = matriz_original[0:r_topo, c_a + c_e : N]

    B = matriz_original[r_topo:M, 0:c_a]
    C = matriz_original[r_topo:M, c_a : c_a + c_e]
    I = matriz_original[r_topo:M, c_a + c_e : N]

    # 2. Reorganização com colunas alinhadas: [I, C, B ; O, E, A]
    matriz_nova = np.block([[I, C, B], [O, E, A]])

    return matriz_nova
