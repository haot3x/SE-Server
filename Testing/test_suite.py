# Tianxiong Jiang (Martin)
# How to use this script:
# 1. Add the url you wish to test in the CONFIG list.
# 2. Configure your host and expected directory 
# 3. Save the expected results with the same as your url in the expected directory 
# 4. Run the script and see the results 



import unittest
import json
import urllib2
import os

HOST = "http://yale-hout.appspot.com" 
EXPECTED_DIR = "expected"

class HoutTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event(self):
        CONFIG = ['534ca3ab58738cfffe20f09d', '5351c2a66c22bdfffeb3f4f9', 
        '5351cbc66c22bdfffeb3f502']

        API = HOST + '/api/event/'
        DIR = os.path.join(EXPECTED_DIR, "event")

        for i in CONFIG:
            url = API + i
            print "Testing URL" + url
            fileName = os.path.join(DIR, i) + '.json'
            obj_api = json.load(urllib2.urlopen(url))
            obj_test = json.load(open(fileName,'r'))

            for k,v in obj_api.items():
                self.assertTrue(v == obj_test[k])

            print "Pass\n"

    def test_xx(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
