import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    def __init__(self, access_code="10101010", payload_len_in_bits=10, threshold=3):
        gr.basic_block.__init__(
            self,
            name='Find access code (soft)',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.access_code = np.array([int(x) for x in access_code])
        self.payload_len_in_bits = payload_len_in_bits
        self.threshold = threshold

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        ac_len = self.access_code.size
        pl_len = self.payload_len_in_bits

        if len(in0) < ac_len + pl_len:
            return 0
        if len(out0) < pl_len:
            return 0

        hard_bits = (in0[:ac_len] > 0).astype(int)
        hamming_dist = np.sum(hard_bits != self.access_code)

        if hamming_dist > self.threshold:
            self.consume(0, 1)
            return 0

        out0[:pl_len] = in0[ac_len: ac_len + pl_len] 
        self.consume(0, ac_len + pl_len)
        return pl_len
