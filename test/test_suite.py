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
        CONFIG = ['535af34e9f5ffcfffe58a801', '535af4cf9f5ffcfffe3ffcbe', 
        '535af6f558738cfffef04d41',
        '535203de6c22bdfffe601d5d','5352cfbc6c22bdfffefa2f76',
        '5355c36c6c22bdfffe6f5dc0', '535aa85b9f5ffcfffe67f3a0',
        '535aacaf6c22bdfffe0f207a','535aadab9f5ffcfffe8f293c',
        '535aae5b58738cfffe020764', '535ab1dc58738cfffebb0812',
        '535aedfa58738cfffeb58926', '535aee2958738cfffeb58927',
        '535aeff66c22bdfffec86a4f', '535af4169f5ffcfffea21c93',
        '535af68458738cfffe7e537c', '535af76f58738cfffed9fe8e']

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
