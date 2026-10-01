import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    def __init__(self, constellation=None, access_code="10101010", payload_len_in_bits=272, threshold=5.0):
        gr.basic_block.__init__(
            self,
            name='Find access code (symbol domain)',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.access_code = access_code
        self.payload_len_in_bits = payload_len_in_bits
        self.threshold = threshold
        self.ref_symbols = np.array([], dtype=np.complex64)
        self.payload_len_in_symbols = 0
        self._min_dist = [float('inf')] * 4
        self._call_count = 0

        if constellation is not None:
            self._setup(constellation)

    def _setup(self, constellation):
        bps = constellation.bits_per_symbol()
        bits = [int(b) for b in self.access_code]
        assert len(bits) % bps == 0

        ref = []
        for i in range(0, len(bits), bps):
            idx = 0
            for b in bits[i:i+bps]:
                idx = (idx << 1) | b
            ref.append(constellation.map_to_points_v(idx)[0])
        base = np.array(ref, dtype=np.complex64)

        # as 4 rotações possíveis da referência
        self.rotations = [base * (1j ** k) for k in range(4)]

        assert self.payload_len_in_bits % bps == 0
        self.payload_len_in_symbols = self.payload_len_in_bits // bps

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        ac_len = self.rotations[0].size
        pl_len = self.payload_len_in_symbols

        if ac_len == 0:
            return 0
        if len(in0) < ac_len + pl_len:
            return 0
        if len(out0) < pl_len:
            return 0

        window = in0[:ac_len]
        dists = [np.sum(np.abs(window - ref)**2) for ref in self.rotations]
        best_k = int(np.argmin(dists))
        best_dist = dists[best_k]

        for k in range(4):
            self._min_dist[k] = min(self._min_dist[k], dists[k])
        self._call_count += 1
        if self._call_count % 2000 == 0:
            print(f"menor dist_sq por rotação (0,90,180,270): {self._min_dist}")
            self._min_dist = [float('inf')] * 4

        if best_dist > self.threshold:
            self.consume(0, 1)
            return 0

        out0[:pl_len] = in0[ac_len: ac_len + pl_len] * (1j ** (-best_k))  # já corrige a rotação no payload
        self.consume(0, ac_len + pl_len)
        return pl_len
