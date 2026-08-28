import numpy as np
import komm

EbN0db = 6
R = 1                                                   # uncoded bpsk
EbN0 = 10**(EbN0db/10)
sigma = np.sqrt(1/(2*R*EbN0))

ch = komm.GaussianChannel(2*sigma**2)
source = komm.DiscreteMemorylessSource([0.5,0.5])
const = komm.PSKConstellation(2)

BER_th = komm.gaussian_q(1/sigma)

N = 1000                                              # numero de bits da mensagem por bloco
Nerrs = 0
Nblocks = 1000

for i in range (Nblocks):
    msg = source.emit(N)                                # cria bits aleatorios
    s = const.indices_to_symbols(msg)                   # BPSK bit to symbol conversion
    r = ch.transmit(s)                                  # canal awgn
    msg_cap = const.closest_indices(r)                  # threshold em 0
    Nerrs += sum(msg != msg_cap)

BER_sim = Nerrs/N/Nblocks

print(f"Ber teo: {BER_th}")
print(f"BER_sim: {BER_sim}")
print(f"Numero de erros: {Nerrs}")
print(f"Numero de transmissões: {N*Nblocks}")
