import numpy as np
import komm

EbN0db = 6
R = 4/7
EbN0 = 10**(EbN0db/10)
sigma = np.sqrt(1/(2*R*EbN0))
rng = np.random.default_rng(seed=42)

ch = komm.GaussianChannel(2*sigma**2, rng=rng)
source = komm.DiscreteMemorylessSource([0.5,0.5])
code = komm.HammingCode(3)
const = komm.PSKConstellation(2)

cwords = code.codewords()

k = code.dimension #numero de message bits
n = code.length #numero de codeword bits

Nbiterrs1 = 0
Nbiterrs2 = 0
Nblockerrs1 = 0
Nblockerrs2 = 0
Nblocks = 100000

cwords_bpsk = const.indices_to_symbols(cwords)      # necessário para soft decoding, modula todas as cwords para bpsk

for i in range (Nblocks):
    msg = source.emit(k)                                # cria bits aleatorios

    # encoding
    cword = code.encode(msg)

    s = const.indices_to_symbols(cword)                 # BPSK bit to symbol conversion
    
    r = ch.transmit(s)                                  # canal awgn

    b = const.closest_indices(r)                        # BPSK symbol to bit conversion

    #hard decision decoding
    dist = np.sum(b ^ cwords, axis=1)                   # calcula as distancias de b para cada uma das cws
    pos = np.argmin(dist)                               # retorna a posicao do menor valor
    msg_cap1 = cwords[pos, :k]                          # pega os primeiros 4 bits (mensagem enviada) da cw mais provavel 

    # soft decision decoding
    correlacao = np.dot(cwords_bpsk.real, r.real)
    pos = np.argmax(correlacao)
    msg_cap2 = cwords[pos, :k]

    Nerrs1 = np.sum(msg != msg_cap1)
    Nerrs2 = np.sum(msg != msg_cap2)

    if Nerrs1 > 0:
        Nbiterrs1 += Nerrs1
        Nblockerrs1 += 1
    if Nerrs2 > 0:
        Nbiterrs2 += Nerrs2
        Nblockerrs2 += 1

BER_sim1 = Nbiterrs1/k/Nblocks
FER_sim1 = Nblockerrs1/Nblocks
BER_sim2 = Nbiterrs2/k/Nblocks
FER_sim2 = Nblockerrs2/Nblocks

print(10*("-") + f"Hard decoding" + 10*("-"))
print(f"BER_sim: {BER_sim1}")
print(f"FER_sim: {FER_sim1}")
print(f"Numero de erros de bits: {Nbiterrs1}")
print(f"Numero de erros de blocos: {Nblockerrs1}")
print(f"Numero de transmissões: {k*Nblocks}")

print(10*("-") + f"Soft decoding" + 10*("-"))
print(f"BER_sim: {BER_sim2}")
print(f"FER_sim: {FER_sim2}")
print(f"Numero de erros de bit: {Nbiterrs2}")
print(f"Numero de erros de blocos: {Nblockerrs2}")
print(f"Numero de transmissões: {k*Nblocks}")