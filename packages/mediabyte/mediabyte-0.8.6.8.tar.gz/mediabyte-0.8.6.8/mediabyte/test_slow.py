#!/home/dd/anaconda3/bin/python

import unittest
from files import lib, yota_fuzz, bit_fuzz

class TestommSlowTests(unittest.TestCase):

    def setUp(self):
        pass


## SEARCH YOUTUBE 50 RESULTS

    def test_search_to_mixtape_50_results(self):
        hakMix = lib.Convert.search_to_mixtape('hak5 50')
        self.assertEqual(len(hakMix.content), 50)


# disable hash_dict adding before running this
# ## YOTA FUZZING 5.000 ROUNDS

#     def test_yota_input_fuzzing_5000_mixtape(self):
#         myFuzzMix = yota_fuzz.main(5000, mixtape=True)
#         self.assertEqual(len(myFuzzMix.content), 5000)

## BIT FUZZING 3 ROUNDS

    # def test_bit_input_fuzzing_3(self):
    #     myFuzzMix = bit_fuzz.main(3)
    #     self.assertEqual(len(myFuzzMix), 3)



if __name__ == '__main__':
    unittest.main()    