#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Verisure (Securitas Direct) - demodulator
# Generated: Sun Nov 16 10:44:20 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cc1111
import math
import osmosdr
import wx

class verisure_demod(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Verisure (Securitas Direct) - demodulator")

        ##################################################
        # Variables
        ##################################################
        self.symbole_rate = symbole_rate = 38450
        self.samp_rate = samp_rate = 2.0e06
        self.rat_interop = rat_interop = 8
        self.rat_decim = rat_decim = 5
        self.frequency_tune = frequency_tune = 17.22e3
        self.frequency_shift = frequency_shift = 0.52e06
        self.frequency_center = frequency_center = 868.5e06
        self.firdes_transition_width = firdes_transition_width = 15000
        self.firdes_decim = firdes_decim = 4
        self.firdes_cutoff = firdes_cutoff = 21e3
        self.samp_per_sym = samp_per_sym = ((samp_rate/2/firdes_decim)*rat_interop/rat_decim) / symbole_rate
        self.rf_gain = rf_gain = 0
        self.myqueue = myqueue = gr.msg_queue(200)
        self.if_gain = if_gain = 20
        self.frequency = frequency = frequency_center + frequency_shift + frequency_tune
        self.freq_display = freq_display = frequency_center + frequency_shift + frequency_tune
        self.firdes_filter = firdes_filter = firdes.low_pass(1,samp_rate/2, firdes_cutoff, firdes_transition_width)
        self.fft_sp = fft_sp = 50000
        self.crc_verbose = crc_verbose = False
        self.bb_gain = bb_gain = 20
        self.access_code = access_code = '11010011100100011101001110010001'

        ##################################################
        # Blocks
        ##################################################
        _rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rf_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label="RF Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rf_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	minimum=0,
        	maximum=14,
        	num_steps=15,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_rf_gain_sizer, 0, 0, 1, 1)
        _if_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._if_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_if_gain_sizer,
        	value=self.if_gain,
        	callback=self.set_if_gain,
        	label="IF Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._if_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_if_gain_sizer,
        	value=self.if_gain,
        	callback=self.set_if_gain,
        	minimum=0,
        	maximum=30,
        	num_steps=31,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_if_gain_sizer, 0, 1, 1, 1)
        _frequency_tune_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frequency_tune_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_frequency_tune_sizer,
        	value=self.frequency_tune,
        	callback=self.set_frequency_tune,
        	label="Frequency Tuning",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._frequency_tune_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_frequency_tune_sizer,
        	value=self.frequency_tune,
        	callback=self.set_frequency_tune,
        	minimum=-30e3,
        	maximum=30e3,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_frequency_tune_sizer, 0, 3, 1, 1)
        _bb_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._bb_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_bb_gain_sizer,
        	value=self.bb_gain,
        	callback=self.set_bb_gain,
        	label="BB Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._bb_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_bb_gain_sizer,
        	value=self.bb_gain,
        	callback=self.set_bb_gain,
        	minimum=0,
        	maximum=30,
        	num_steps=31,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_bb_gain_sizer, 0, 2, 1, 1)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency_center + frequency_shift + frequency_tune,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=fft_sp,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT",
        	peak_hold=True,
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 2, 0, 1, 4)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=rat_interop,
                decimation=rat_decim,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=int(samp_rate/2/fft_sp),
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "hackrf=0" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(frequency_center, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(2, (1, ), frequency_shift+frequency_tune, samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(firdes_decim, (firdes_filter), 0, samp_rate/2)
        self._freq_display_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.freq_display,
        	callback=self.set_freq_display,
        	label="Current Frequency",
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._freq_display_static_text, 1, 0, 1, 4)
        self.digital_correlate_access_code_bb_0_0 = digital.correlate_access_code_bb(access_code, 1)
        self.digital_clock_recovery_mm_xx_0_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0_0_0 = digital.binary_slicer_fb()
        self.cc1111_cc1111_packet_decoder_0 = cc1111.cc1111_packet_decoder(myqueue,True, True, False, False)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0_0, 0), (self.digital_correlate_access_code_bb_0_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0_0, 0), (self.digital_binary_slicer_fb_0_0_0, 0))
        self.connect((self.digital_correlate_access_code_bb_0_0, 0), (self.cc1111_cc1111_packet_decoder_0, 0))
        self.connect((self.cc1111_cc1111_packet_decoder_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.digital_clock_recovery_mm_xx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))



    def get_symbole_rate(self):
        return self.symbole_rate

    def set_symbole_rate(self, symbole_rate):
        self.symbole_rate = symbole_rate
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cutoff, self.firdes_transition_width))
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_rat_interop(self):
        return self.rat_interop

    def set_rat_interop(self, rat_interop):
        self.rat_interop = rat_interop
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_rat_decim(self):
        return self.rat_decim

    def set_rat_decim(self, rat_decim):
        self.rat_decim = rat_decim
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_frequency_tune(self):
        return self.frequency_tune

    def set_frequency_tune(self, frequency_tune):
        self.frequency_tune = frequency_tune
        self.set_frequency(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self._frequency_tune_slider.set_value(self.frequency_tune)
        self._frequency_tune_text_box.set_value(self.frequency_tune)
        self.set_freq_display(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.frequency_shift+self.frequency_tune)
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency_center + self.frequency_shift + self.frequency_tune)

    def get_frequency_shift(self):
        return self.frequency_shift

    def set_frequency_shift(self, frequency_shift):
        self.frequency_shift = frequency_shift
        self.set_frequency(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self.set_freq_display(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.frequency_shift+self.frequency_tune)
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency_center + self.frequency_shift + self.frequency_tune)

    def get_frequency_center(self):
        return self.frequency_center

    def set_frequency_center(self, frequency_center):
        self.frequency_center = frequency_center
        self.set_frequency(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self.set_freq_display(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self.osmosdr_source_0.set_center_freq(self.frequency_center, 0)
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency_center + self.frequency_shift + self.frequency_tune)

    def get_firdes_transition_width(self):
        return self.firdes_transition_width

    def set_firdes_transition_width(self, firdes_transition_width):
        self.firdes_transition_width = firdes_transition_width
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cutoff, self.firdes_transition_width))

    def get_firdes_decim(self):
        return self.firdes_decim

    def set_firdes_decim(self, firdes_decim):
        self.firdes_decim = firdes_decim
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_firdes_cutoff(self):
        return self.firdes_cutoff

    def set_firdes_cutoff(self, firdes_cutoff):
        self.firdes_cutoff = firdes_cutoff
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cutoff, self.firdes_transition_width))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_clock_recovery_mm_xx_0_0.set_omega(self.samp_per_sym*(1+0.0))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_slider.set_value(self.rf_gain)
        self._rf_gain_text_box.set_value(self.rf_gain)
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_myqueue(self):
        return self.myqueue

    def set_myqueue(self, myqueue):
        self.myqueue = myqueue

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self._if_gain_slider.set_value(self.if_gain)
        self._if_gain_text_box.set_value(self.if_gain)
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_freq_display(self):
        return self.freq_display

    def set_freq_display(self, freq_display):
        self.freq_display = freq_display
        self._freq_display_static_text.set_value(self.freq_display)

    def get_firdes_filter(self):
        return self.firdes_filter

    def set_firdes_filter(self, firdes_filter):
        self.firdes_filter = firdes_filter
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((self.firdes_filter))

    def get_fft_sp(self):
        return self.fft_sp

    def set_fft_sp(self, fft_sp):
        self.fft_sp = fft_sp
        self.wxgui_fftsink2_0.set_sample_rate(self.fft_sp)

    def get_crc_verbose(self):
        return self.crc_verbose

    def set_crc_verbose(self, crc_verbose):
        self.crc_verbose = crc_verbose

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self._bb_gain_slider.set_value(self.bb_gain)
        self._bb_gain_text_box.set_value(self.bb_gain)
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = verisure_demod()
    tb.Start(True)
    tb.Wait()
