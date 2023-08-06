"""
file: list_mode_data_decoder_tests.py
brief: Unittests for the list_mode_data_decoder class.
author: S. V. Paulauskas
date: March 5, 2019
"""
from io import BytesIO
import unittest

import dolosse.hardware.xia.pixie16.list_mode_data_decoder as decoder
import dolosse.hardware.xia.pixie16.list_mode_data_mask as lmdm


# TODO : We'll need to add tests to cover the major firmware revisions.
class ListModeDataDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.mask = lmdm.ListModeDataMask(250, 30474)

    def test_decode_word_zero(self):
        self.assertEqual({
            'channel': 13,
            'slot': 2,
            'crate': 0,
            'header_length': 4,
            'event_length': 4,
            'finish_code': 0
        }, decoder.decode_word_zero(540717, self.mask))

    def test_decode_word_two(self):
        self.assertEqual({
            'event_time_high': 26001,
            'cfd_fractional_time': 0,
            'cfd_trigger_source_bit': 0,
            'cfd_forced_trigger_bit': 0
        }, decoder.decode_word_two(26001, self.mask))

    def test_decode_word_three(self):
        self.assertEqual({
            'energy': 2345,
            'trace_length': 0,
            'trace_out_of_range': 0
        }, decoder.decode_word_three(2345, self.mask))

    def test_run(self):
        self.assertEqual(
            decoder.ListModeDataDecoder(
                BytesIO(b'\x2D\x40\x08\x00\x15\xCD\x5B\x07\x91\x65\x00\x00\x29\x09\x00\x00'),
                self.mask).run(),
            [{
                'channel': 13,
                'slot': 2,
                'crate': 0,
                'header_length': 4,
                'event_length': 4,
                'finish_code': 0,
                'event_time_low': 123456789,
                'event_time_high': 26001,
                'cfd_fractional_time': 0,
                'cfd_trigger_source_bit': 0,
                'cfd_forced_trigger_bit': 0,
                'energy': 2345,
                'trace_length': 0,
                'trace_out_of_range': 0
            }])


if __name__ == '__main__':
    unittest.main()
