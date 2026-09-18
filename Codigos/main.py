import numpy as np
from alist import *
from matriz import *

ZC_SETS = {
    0: [2, 4, 8, 16, 32, 64, 128, 256],
    1: [3, 6, 12, 24, 48, 96, 192, 384],
    2: [5, 10, 20, 40, 80, 160, 320],
    3: [7, 14, 28, 56, 112, 224],
    4: [9, 18, 36, 72, 144, 288],
    5: [11, 22, 44, 88, 176, 352],
    6: [13, 26, 52, 104, 208],
    7: [15, 30, 60, 120, 240],
}

bg = int(input("Informe BG (1 ou 2): "))
ils = int(input("Informe i_LS (0 a 7): "))
zc = int(input("Informe Z_c (Fator de expansão): "))

if zc in ZC_SETS[ils]:
    if (bg == 1 or bg == 2):
        v = np.loadtxt(f"../v_matrices/NR_{bg}_{ils}_{ZC_SETS[ils][-1]}.txt", dtype=int)
        v_org = reorganizar_bg(v)
        np.savetxt(f"../v_inv_matrices/NR_{bg}_{ils}_{ZC_SETS[ils][-1]}.txt", v_org, fmt="%d", delimiter= " ")
        base_matrix = protograph(bg, ils, zc, f"../v_inv_matrices")
        protograph_to_alist(base_matrix, zc, f"../alists/NR_{bg}_{ils}_{zc}_{zc*4}.alist")
    else:
        print("bg invalido")
else:
    print("Conjunto Z_c + i_LS inválido")
