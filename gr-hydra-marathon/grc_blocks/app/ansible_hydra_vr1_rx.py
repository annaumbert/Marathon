#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ansible Hydra Vr1 Rx
# Generated: Mon Oct 14 19:35:01 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import SimpleXMLRPCServer
import sys
import threading
import time
from gnuradio import qtgui


class ansible_hydra_vr1_rx(gr.top_block, Qt.QWidget):

    def __init__(self, ansibleIP='192.168.5.78', freqrx=2.48e9, freqtx=2.48e9+3e6, gain=0.85, samp_rate=400e3, vr1offset=-300e3, vr2offset=300e3):
        gr.top_block.__init__(self, "Ansible Hydra Vr1 Rx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ansible Hydra Vr1 Rx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "ansible_hydra_vr1_rx")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Parameters
        ##################################################
        self.ansibleIP = ansibleIP
        self.freqrx = freqrx
        self.freqtx = freqtx
        self.gain = gain
        self.samp_rate = samp_rate
        self.vr1offset = vr1offset
        self.vr2offset = vr2offset

        ##################################################
        # Variables
        ##################################################
        self.mul = mul = 0.04

        ##################################################
        # Blocks
        ##################################################
        self._mul_range = Range(0, 1, 0.01, 0.04, 200)
        self._mul_win = RangeWidget(self._mul_range, self.set_mul, 'mul', "counter_slider", float)
        self.top_layout.addWidget(self._mul_win)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer((ansibleIP, 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freqrx + vr1offset, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freqtx + vr1offset, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.digital_ofdm_tx_0_0 = digital.ofdm_tx(
        	  fft_len=64, cp_len=16,
        	  packet_length_tag_key="len",
        	  bps_header=1,
        	  bps_payload=1,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_rx_0_0 = digital.ofdm_rx(
        	  fft_len=64, cp_len=16,
        	  frame_length_tag_key='frame_'+"len",
        	  packet_length_tag_key="len",
        	  bps_header=1,
        	  bps_payload=1,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.blocks_tuntap_pdu_1_0 = blocks.tuntap_pdu('tap0', 200, False)
        self.blocks_tagged_stream_to_pdu_0_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "len")
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, 'VR1 RX', ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "len")
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((mul, ))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0, 'pdus'), (self.blocks_tuntap_pdu_1_0, 'pdus'))
        self.msg_connect((self.blocks_tuntap_pdu_1_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.digital_ofdm_tx_0_0, 0))
        self.connect((self.digital_ofdm_rx_0_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_ofdm_rx_0_0, 0), (self.blocks_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.digital_ofdm_tx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_ofdm_rx_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ansible_hydra_vr1_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_ansibleIP(self):
        return self.ansibleIP

    def set_ansibleIP(self, ansibleIP):
        self.ansibleIP = ansibleIP

    def get_freqrx(self):
        return self.freqrx

    def set_freqrx(self, freqrx):
        self.freqrx = freqrx
        self.uhd_usrp_source_0.set_center_freq(self.freqrx + self.vr1offset, 0)

    def get_freqtx(self):
        return self.freqtx

    def set_freqtx(self, freqtx):
        self.freqtx = freqtx
        self.uhd_usrp_sink_0.set_center_freq(self.freqtx + self.vr1offset, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_normalized_gain(self.gain, 0)


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_vr1offset(self):
        return self.vr1offset

    def set_vr1offset(self, vr1offset):
        self.vr1offset = vr1offset
        self.uhd_usrp_source_0.set_center_freq(self.freqrx + self.vr1offset, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.freqtx + self.vr1offset, 0)

    def get_vr2offset(self):
        return self.vr2offset

    def set_vr2offset(self, vr2offset):
        self.vr2offset = vr2offset

    def get_mul(self):
        return self.mul

    def set_mul(self, mul):
        self.mul = mul
        self.blocks_multiply_const_vxx_0_0.set_k((self.mul, ))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--ansibleIP", dest="ansibleIP", type="string", default='192.168.5.78',
        help="Set ansibleIP [default=%default]")
    return parser


def main(top_block_cls=ansible_hydra_vr1_rx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(ansibleIP=options.ansibleIP)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
