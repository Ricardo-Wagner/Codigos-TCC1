import numpy as np
from pathlib import Path
from Generate_LDPC_matrix_functions import *
# --- Tabela 5.3.2-1 do 3GPP TS 38.212: conjuntos válidos de Zc por i_LS ---
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

def load_raw_V(i, i_LS, table_dir="v_matrices"):
    """
    Carrega a tabela crua V(r,c) — que é simplesmente o arquivo do
    Zc MÁXIMO daquele i_LS (ex: NR_1_0_256.txt), já que V é
    definido com valores < Zc_max, então V mod Zc_max = V.
    """
    zc_max = ZC_SETS[i_LS][-1]
    path = f"{table_dir}/NR_{i}_{i_LS}_{zc_max}.txt"
    return np.loadtxt(path, dtype=int)


def protograph(i=1, i_LS=0, Zc=2, table_dir="v_matrices"):
    if Zc not in ZC_SETS[i_LS]:
        raise ValueError(f"Zc={Zc} não pertence ao i_LS={i_LS}. "
                          f"Válidos: {ZC_SETS[i_LS]}")
    V = load_raw_V(i, i_LS, table_dir)
    return np.where(V == -1, -1, V % Zc)


def expand_protograph(base_matrix, Zc):
    """Faz o lifting: expande a matriz base em H binária completa."""
    numRowsB, numColsB = base_matrix.shape
    H = np.zeros((numRowsB * Zc, numColsB * Zc))
    I = np.identity(Zc)

    for r in range(numRowsB):
        for c in range(numColsB):
            shift = int(base_matrix[r, c])
            if shift == -1:
                continue
            H[r*Zc:(r+1)*Zc, c*Zc:(c+1)*Zc] = np.roll(I, shift, axis=1)
    return H


def protograph_to_alist(protograph, Zc, output_file):
    """
    Expande o protograph (via lifting) e escreve o .alist,
    reaproveitando a write_alist_file já validada do GNU Radio.
    """
    H = expand_protograph(protograph, Zc)
    bestH, gap = get_best_matrix(H, numIterations=50)
    write_alist_file(output_file, bestH)
    return bestH, gap
