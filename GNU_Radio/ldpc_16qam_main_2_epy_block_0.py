import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    def __init__(self, constellation=None, access_code="10101010", payload_len_in_bits=272, threshold=5.0):
        gr.basic_block.__init__(
            self,
            name='Find access code + soft decode (symbol domain)',
            in_sig=[np.complex64],
            out_sig=[np.float32]
        )
        self.access_code = access_code
        self.payload_len_in_bits = payload_len_in_bits
        self.threshold = threshold

        self.constellation = None
        self.rotations = []
        self.payload_len_in_symbols = 0
        self.bits_per_symbol = 0

        self._min_dist = [float('inf')] * 4
        self._call_count = 0
        self._last_npwr = None

        if constellation is not None:
            self._setup(constellation)

    def _setup(self, constellation):
        self.constellation = constellation
        bps = constellation.bits_per_symbol()
        self.bits_per_symbol = bps

        bits = [int(b) for b in self.access_code]
        assert len(bits) % bps == 0, "access_code precisa ser múltiplo de bits_per_symbol"

        ref = []
        for i in range(0, len(bits), bps):
            idx = 0
            for b in bits[i:i + bps]:
                idx = (idx << 1) | b
            ref.append(constellation.map_to_points_v(idx)[0])
        base = np.array(ref, dtype=np.complex64)

        # as 4 rotações possíveis da referência (simetria de ordem 4 do 16QAM)
        self.rotations = [base * (1j ** k) for k in range(4)]

        assert self.payload_len_in_bits % bps == 0
        self.payload_len_in_symbols = self.payload_len_in_bits // bps

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]

        if not self.rotations:
            # ainda não inicializado de verdade (ex.: passada de descoberta do GRC)
            return 0

        ac_len = self.rotations[0].size
        pl_len = self.payload_len_in_symbols
        out_len_needed = pl_len * self.bits_per_symbol

        if len(in0) < ac_len + pl_len:
            return 0
        if len(out0) < out_len_needed:
            return 0

        window = in0[:ac_len]
        dists = [np.sum(np.abs(window - ref) ** 2) for ref in self.rotations]
        best_k = int(np.argmin(dists))
        best_dist = dists[best_k]

        # --- diagnóstico opcional (pode remover depois de validar) ---
        for k in range(4):
            self._min_dist[k] = min(self._min_dist[k], dists[k])
        self._call_count += 1
        if self._call_count % 2000 == 0:
            print(f"menor dist_sq por rotação (0,90,180,270): {self._min_dist}  "
                  f"| último npwr medido: {self._last_npwr}")
            self._min_dist = [float('inf')] * 4
        # ---------------------------------------------------------------

        if best_dist > self.threshold:
            self.consume(0, 1)
            return 0

        # ruído medido na própria janela do access code que acabou de bater
        measured_npwr = max(best_dist / ac_len, 1e-6)
        self._last_npwr = measured_npwr

        # corrige a rotação nos símbolos do payload
        payload_symbols = in0[ac_len: ac_len + pl_len] * (1j ** (-best_k))

        # decisão soft símbolo a símbolo, usando o ruído medido agora
        soft_bits = np.concatenate([
            self.constellation.calc_soft_dec(sym, measured_npwr)
            for sym in payload_symbols
        ]).astype(np.float32)

        out0[:out_len_needed] = soft_bits
        self.consume(0, ac_len + pl_len)
        return out_len_needed
