import numpy as np
import komm

EbN0db = 6
R = 1/3                                             # n=3 repetition code
EbN0 = 10**(EbN0db/10)
sigma = np.sqrt(1/(2*R*EbN0))
rng = np.random.default_rng(seed=42)

ch = komm.GaussianChannel(2*sigma**2, rng=rng)
source = komm.DiscreteMemorylessSource([0.5,0.5])
code = komm.RepetitionCode(3)
const = komm.PSKConstellation(2)

k = 1 #numero de message bits
n = 3 #numero de codeword bits

Nerrs1 = 0
Nerrs2 = 0
Nblocks = 100000

for i in range (Nblocks):
    msg = source.emit(k)                                # cria bits aleatorios

    # encoding
    cword = code.encode(msg)

    s = const.indices_to_symbols(cword)                 # BPSK bit to symbol conversion
    
    r = ch.transmit(s)                                  # canal awgn

    b = const.closest_indices(r)                        # BPSK symbol to bit conversion

    #hard decision decoding
    if np.sum(b) > 1:
        msg_cap1 = 1
    else:
        msg_cap1 = 0

    # soft decision decoding
    if np.sum(r.real) < 0:
        msg_cap2 = 1
    else:
        msg_cap2 = 0

    Nerrs1 += np.sum(msg != msg_cap1)
    Nerrs2 += np.sum(msg != msg_cap2)

BER_sim1 = Nerrs1/k/Nblocks
BER_sim2 = Nerrs2/k/Nblocks

print(10*("-") + f"Hard decoding" + 10*("-"))
print(f"BER_sim: {BER_sim1}")
print(f"Numero de erros: {Nerrs1}")
print(f"Numero de transmissões: {k*Nblocks}")

print(10*("-") + f"Soft decoding" + 10*("-"))
print(f"BER_sim: {BER_sim2}")
print(f"Numero de erros: {Nerrs2}")
print(f"Numero de transmissões: {k*Nblocks}")
