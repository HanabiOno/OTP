from crack import(
    isngram
    isenglishword
    findwordswithsequence
    addwordtodatindex
)
from otp import (
    one_time_pad,
    otp_encrypt,
    subtract_modulo_alphabet,
    add_modulo_alphabet,
)
import unittest

plaintext1 = "the cat sat on the mat"
plaintext2 = "happy birthday to you"
otp0 = one_time_pad(max(len(plaintext1), len(plaintext2)))
cyphertext1, _ = otp_encrypt(plaintext1, otp0)
cyphertext2, _ = otp_encrypt(plaintext2, otp0)
d = subtract_modulo_alphabet(cyphertext2, cyphertext1)

class TestPM(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_ing_trigram(self):
        self.assertEqual(isngram("ing"), True)

    def test_is_xvcq_quadgram(self):
        self.assertEqual(isngram("xvcq"), False)

    def test_is_iNg_trigram(self):
        self.asserEqual(isngram("iNg"), True)

    def test_is_english_though(self):
        self.assertEqual(isenglishword("though"), True)

    def test_is_english_thinks(self):
        self.assertEqual(isenglishword("thinks"), False)

    def test_is_english_gr(self):
        self.assertEqual(isenglishword("gr"), False)

    def test_add_cat_to_d_at_4:
        self.asserEqual(addwordtodatindex(d, "cat", 4), "y b")                                

if __name__ == '__main__':
    unittest.main()
