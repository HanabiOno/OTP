from crack import(
    isngram,
    isenglishword,
    findwordswithsequence,
    addwordtodatindex,
    replacer,
    str_indexer,
    str_returner,
    collision_finder,
    couldbeenglish,
    pop_dict_creator,
    chooser,
    finder
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
lst = [[0, 'T'], [1, 'h'], [2, 'e'], [3, ' '], [4, 'c'], [5, 'a'], [6, 't']]
popularity_dict = {} 
book_list_1 =[ '../book1.txt', '../book2.txt', '../book3.txt', '../book4.txt', '../book5.txt']
popularity_dict =  pop_dict_creator(book_list_1, popularity_dict)


class TestPM(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_ing_trigram(self):
        self.assertEqual(isngram("ing"), True)

    def test_is_xvcq_quadgram(self):
        self.assertEqual(isngram("xvcq"), False)

    def test_is_iNg_trigram(self):
        self.assertEqual(isngram("iNg"), True)

    def test_is_english_though(self):
        self.assertEqual(isenglishword("though"), True)

    def test_is_english_thinks(self):
        self.assertEqual(isenglishword("thinks"), True)

    def test_is_english_gr(self):
        self.assertEqual(isenglishword("gr"), False)

    def test_add_cat_to_d_at_4(self):
        self.assertEqual(addwordtodatindex(d, "cat", 4), "y b")

    def str_indexer(self):
        self.assertEqual(str_indexer('The cat'), lst, [6, 't']) 

    def test_replacer(self):
         self.assertEqual(replacer('fox', 4,lst), [[0, 'T'], [1, 'h'], [2, 'e'], [3, ' '], [4, 'f'], [5, 'o'], [6, 'x']])

    def test_str_returner(self):
        self.assertEqual(str_returner(lst), 'The cat')
        
    def test_collision_finder(self): 
        self.assertEqual(collision_finder(lst, 'fox', 3), [True, 4])

    def test_couldbeenglish_good(self):
        self.assertEqual(couldbeenglish("ing, wi", simple = True), True)

    def test_couldbeenglish_capital(self):
        self.assertEqual(couldbeenglish("inG, wi", simple = True), False)

    def test_couldbeenglish_dubblepunct(self):
        self.assertEqual(couldbeenglish("ing,.  wi", simple = True), False)

    def test_couldbeenglish_numberinbetween(self):
        self.assertEqual(couldbeenglish("in9, wi", simple = True), False)

    def test_couldbeenglish_I(self):
        self.assertEqual(couldbeenglish("I", simple = True), True)

    def test_couldbeenglish_capitalafterpunct(self):
        self.assertEqual(couldbeenglish("ing.Wi", simple = True), False)

    def test_finder(self):
        self.assertEqual(finder(lst, 4), 4)
        
    def test_chooser1(self): 
        self.assertEqual(chooser('hello', 'interview', popularity_dict), 'interview')
    
    def test_chooser2(self): 
        self.assertEqual(chooser('johannesburg', 'neuroscience', popularity_dict), 'neuroscience')


if __name__ == '__main__':
    unittest.main()
