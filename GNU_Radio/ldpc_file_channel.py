#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ldpc_file_channel
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import filter
from gnuradio import fec
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import ldpc_file_channel_epy_block_0 as epy_block_0  # embedded python block
import numpy as np
import sip
import threading



class ldpc_file_channel(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "ldpc_file_channel", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("ldpc_file_channel")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ldpc_file_channel")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.bits_per_symbol = bits_per_symbol = 1
        self.bit_rate = bit_rate = 800e3
        self.z = z = 16
        self.sps = sps = 10
        self.ils = ils = 0
        self.gap = gap = 1
        self.bg = bg = 1
        self.baud_rate = baud_rate = bit_rate/bits_per_symbol
        self.samp_rate = samp_rate = baud_rate*sps
        self.path_alist = path_alist = "../alists/NR_{}_{}_{}_{}.alist".format(bg, ils, z, gap)
        self.rrc_filter_taps = rrc_filter_taps = firdes.root_raised_cosine(sps, samp_rate,baud_rate, 0.25, (11*sps))
        self.ldpc_H_matrix = ldpc_H_matrix = fec.ldpc_H_matrix(path_alist, gap)
        self.taps = taps = np.array(rrc_filter_taps)
        self.preambulo = preambulo = 32
        self.payload_len = payload_len = 68*z
        self.noise_voltage = noise_voltage = 0
        self.ldpc_encoder = ldpc_encoder = fec.ldpc_par_mtrx_encoder_make_H(ldpc_H_matrix)
        self.ldpc_decoder = ldpc_decoder = fec.ldpc_decoder.make(path_alist, 10)
        self.const = const = digital.constellation_bpsk().base()
        self.const.set_npwr(1.0)
        self.access_code = access_code = "11100001010110101110100010010011"
        self.K = K = 22*z

        ##################################################
        # Blocks
        ##################################################

        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'Transmissor')
        self.tabs_widget_1 = Qt.QWidget()
        self.tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_1)
        self.tabs_grid_layout_1 = Qt.QGridLayout()
        self.tabs_layout_1.addLayout(self.tabs_grid_layout_1)
        self.tabs.addTab(self.tabs_widget_1, 'Receptor')
        self.top_layout.addWidget(self.tabs)
        self._noise_voltage_range = qtgui.Range(0, 8, 0.1, 0, 200)
        self._noise_voltage_win = qtgui.RangeWidget(self._noise_voltage_range, self.set_noise_voltage, "'noise_voltage'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_voltage_win)
        self.qtgui_sink_x_1_0 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1_0.set_update_time(1.0/10)
        self._qtgui_sink_x_1_0_win = sip.wrapinstance(self.qtgui_sink_x_1_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1_0.enable_rf_freq(False)

        self.tabs_grid_layout_0.addWidget(self._qtgui_sink_x_1_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.tabs_grid_layout_0.addWidget(self._qtgui_sink_x_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_sink_x_0_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0_0.enable_rf_freq(False)

        self.tabs_grid_layout_1.addWidget(self._qtgui_sink_x_0_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.tabs_grid_layout_1.addWidget(self._qtgui_sink_x_0_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_1.setColumnStretch(c, 1)
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_char, 1, '127.0.0.1', 2000,2)
        self.interp_fir_filter_xxx_1 = filter.interp_fir_filter_ccc(1, taps/sps)
        self.interp_fir_filter_xxx_1.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(sps, taps)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fec_extended_encoder_0 = fec.extended_encoder(encoder_obj_list=ldpc_encoder, threading='capillary', puncpat='11')
        self.fec_extended_decoder_0 = fec.extended_decoder(decoder_obj_list=ldpc_decoder, threading='capillary', ann=None, puncpat='11', integration_period=10000)
        self.epy_block_0 = epy_block_0.blk(access_code=access_code, payload_len_in_bits=payload_len, threshold=2)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            sps,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(const, -1)
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(const)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_voltage,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((0xE1, 0x5A, 0xE8, 0x93), True, 1, [])
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_char*1, bit_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * bit_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, (preambulo + payload_len), "quadro")
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (preambulo,payload_len))
        self.blocks_pack_k_bits_bb_1 = blocks.pack_k_bits_bb(bits_per_symbol)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'alice.txt', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_sink_x_1_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_1, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.blocks_pack_k_bits_bb_1, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.fec_extended_encoder_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.interp_fir_filter_xxx_1, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.epy_block_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.epy_block_0, 0), (self.fec_extended_decoder_0, 0))
        self.connect((self.fec_extended_decoder_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.fec_extended_encoder_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.qtgui_sink_x_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ldpc_file_channel")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_bits_per_symbol(self):
        return self.bits_per_symbol

    def set_bits_per_symbol(self, bits_per_symbol):
        self.bits_per_symbol = bits_per_symbol
        self.set_baud_rate(self.bit_rate/self.bits_per_symbol)

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.set_baud_rate(self.bit_rate/self.bits_per_symbol)
        self.blocks_throttle2_0_0.set_sample_rate(self.bit_rate)

    def get_z(self):
        return self.z

    def set_z(self, z):
        self.z = z
        self.set_K(22*self.z)
        self.set_path_alist("../alists/NR_{}_{}_{}_{}.alist".format(self.bg, self.ils, self.z, self.gap))
        self.set_payload_len(68*self.z)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_filter_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.baud_rate, 0.25, (11*self.sps)))
        self.set_samp_rate(self.baud_rate*self.sps)
        self.digital_symbol_sync_xx_0.set_sps(self.sps)
        self.interp_fir_filter_xxx_1.set_taps(self.taps/self.sps)

    def get_ils(self):
        return self.ils

    def set_ils(self, ils):
        self.ils = ils
        self.set_path_alist("../alists/NR_{}_{}_{}_{}.alist".format(self.bg, self.ils, self.z, self.gap))

    def get_gap(self):
        return self.gap

    def set_gap(self, gap):
        self.gap = gap
        self.set_path_alist("../alists/NR_{}_{}_{}_{}.alist".format(self.bg, self.ils, self.z, self.gap))

    def get_bg(self):
        return self.bg

    def set_bg(self, bg):
        self.bg = bg
        self.set_path_alist("../alists/NR_{}_{}_{}_{}.alist".format(self.bg, self.ils, self.z, self.gap))

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_rrc_filter_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.baud_rate, 0.25, (11*self.sps)))
        self.set_samp_rate(self.baud_rate*self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rrc_filter_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.baud_rate, 0.25, (11*self.sps)))
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_0_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_1_0.set_frequency_range(0, self.samp_rate)

    def get_path_alist(self):
        return self.path_alist

    def set_path_alist(self, path_alist):
        self.path_alist = path_alist

    def get_rrc_filter_taps(self):
        return self.rrc_filter_taps

    def set_rrc_filter_taps(self, rrc_filter_taps):
        self.rrc_filter_taps = rrc_filter_taps
        self.set_taps(np.array(self.rrc_filter_taps))

    def get_ldpc_H_matrix(self):
        return self.ldpc_H_matrix

    def set_ldpc_H_matrix(self, ldpc_H_matrix):
        self.ldpc_H_matrix = ldpc_H_matrix

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.interp_fir_filter_xxx_0.set_taps(self.taps)
        self.interp_fir_filter_xxx_1.set_taps(self.taps/self.sps)

    def get_preambulo(self):
        return self.preambulo

    def set_preambulo(self, preambulo):
        self.preambulo = preambulo
        self.blocks_stream_to_tagged_stream_0.set_packet_len((self.preambulo + self.payload_len))
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt((self.preambulo + self.payload_len))

    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len((self.preambulo + self.payload_len))
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt((self.preambulo + self.payload_len))
        self.epy_block_0.payload_len_in_bits = self.payload_len

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.channels_channel_model_0.set_noise_voltage(self.noise_voltage)

    def get_ldpc_encoder(self):
        return self.ldpc_encoder

    def set_ldpc_encoder(self, ldpc_encoder):
        self.ldpc_encoder = ldpc_encoder

    def get_ldpc_decoder(self):
        return self.ldpc_decoder

    def set_ldpc_decoder(self, ldpc_decoder):
        self.ldpc_decoder = ldpc_decoder

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const
        self.digital_constellation_encoder_bc_0.set_constellation(self.const)
        self.digital_constellation_soft_decoder_cf_0.set_constellation(self.const)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.epy_block_0.access_code = self.access_code

    def get_K(self):
        return self.K

    def set_K(self, K):
        self.K = K




def main(top_block_cls=ldpc_file_channel, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
