#!/home/dd/anaconda3/bin/python

import unittest
from files import yota_fuzz

class TestommMedium(unittest.TestCase):

    def setUp(self):
        pass

# disable hash_dict adding before running this
# ## YOTA FUZZING

#     def test_yota_input_fuzzing_5000(self):
#         myFuzzList = yota_fuzz.main(5000)
#         self.assertEqual(len(myFuzzList), 5000)


if __name__ == '__main__':
    unittest.main()    
