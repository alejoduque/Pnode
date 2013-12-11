#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: RTL-SDR to Pure Data
# Author: Nicolas Montgermont
# Generated: Wed Oct 17 13:39:04 2012
##################################################

from gnuradio import blks2
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import threading
import time
import wx

class sdr2pd(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="RTL-SDR to Pure Data")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 1920000
		self.cur_freq_fine = cur_freq_fine = 0
		self.cur_freq = cur_freq = 0
		self.channels_coeffs_0 = channels_coeffs_0 = gr.firdes.low_pass(1.0,samp_rate,20000,25000,gr.firdes.WIN_HAMMING)
		self.channels_coeffs = channels_coeffs = gr.firdes.low_pass(1.0,samp_rate,20000,45000,gr.firdes.WIN_HAMMING)

		##################################################
		# Blocks
		##################################################
		self.signal_cur = gr.probe_signal_f()
		self.fine_cur = gr.probe_signal_f()
		self.rtlsdr_source_c_0 = osmosdr.source_c( args="nchan=" + str(1) + " " + "" )
		self.rtlsdr_source_c_0.set_sample_rate(samp_rate)
		self.rtlsdr_source_c_0.set_center_freq(78000000, 0)
		self.rtlsdr_source_c_0.set_freq_corr(0, 0)
		self.rtlsdr_source_c_0.set_gain_mode(0, 0)
		self.rtlsdr_source_c_0.set_gain(10, 0)
		self.rtlsdr_source_c_0.set_if_gain(24, 0)
			
		self.gr_udp_source_0_0 = gr.udp_source(gr.sizeof_float*1, "127.0.0.1", 2001, 4, True, True)
		self.gr_udp_source_0 = gr.udp_source(gr.sizeof_float*1, "127.0.0.1", 2000, 4, True, True)
		self.gr_udp_sink_0_0 = gr.udp_sink(gr.sizeof_float*2048, "127.0.0.1", 2002, 11776, True)
		self.fft_vxx_0 = fft.fft_vcc(2048, True, (window.blackmanharris(1024)), True, 1)
		def _cur_freq_fine_probe():
			while True:
				val = self.fine_cur.level()
				try: self.set_cur_freq_fine(val)
				except AttributeError, e: pass
				time.sleep(1.0/(10))
		_cur_freq_fine_thread = threading.Thread(target=_cur_freq_fine_probe)
		_cur_freq_fine_thread.daemon = True
		_cur_freq_fine_thread.start()
		def _cur_freq_probe():
			while True:
				val = self.signal_cur.level()
				try: self.set_cur_freq(val)
				except AttributeError, e: pass
				time.sleep(1.0/(10))
		_cur_freq_thread = threading.Thread(target=_cur_freq_probe)
		_cur_freq_thread.daemon = True
		_cur_freq_thread.start()
		self.blocks_nlog10_ff_0 = blocks.nlog10_ff(1, 2048, 0)
		self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(2048)
		self.blks2_stream_to_vector_decimator_0 = blks2.stream_to_vector_decimator(
			item_size=gr.sizeof_gr_complex,
			sample_rate=samp_rate,
			vec_rate=25,
			vec_len=2048,
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
		self.connect((self.blks2_stream_to_vector_decimator_0, 0), (self.fft_vxx_0, 0))
		self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
		self.connect((self.rtlsdr_source_c_0, 0), (self.blks2_stream_to_vector_decimator_0, 0))
		self.connect((self.gr_udp_source_0_0, 0), (self.fine_cur, 0))
		self.connect((self.gr_udp_source_0, 0), (self.signal_cur, 0))
		self.connect((self.blocks_nlog10_ff_0, 0), (self.gr_udp_sink_0_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_channels_coeffs_0(gr.firdes.low_pass(1.0,self.samp_rate,20000,25000,gr.firdes.WIN_HAMMING))
		self.set_channels_coeffs(gr.firdes.low_pass(1.0,self.samp_rate,20000,45000,gr.firdes.WIN_HAMMING))
		self.rtlsdr_source_c_0.set_sample_rate(self.samp_rate)
		self.blks2_stream_to_vector_decimator_0.set_sample_rate(self.samp_rate)

	def get_cur_freq_fine(self):
		return self.cur_freq_fine

	def set_cur_freq_fine(self, cur_freq_fine):
		self.cur_freq_fine = cur_freq_fine

	def get_cur_freq(self):
		return self.cur_freq

	def set_cur_freq(self, cur_freq):
		self.cur_freq = cur_freq

	def get_channels_coeffs_0(self):
		return self.channels_coeffs_0

	def set_channels_coeffs_0(self, channels_coeffs_0):
		self.channels_coeffs_0 = channels_coeffs_0

	def get_channels_coeffs(self):
		return self.channels_coeffs

	def set_channels_coeffs(self, channels_coeffs):
		self.channels_coeffs = channels_coeffs

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = sdr2pd()
	tb.Run(True)

