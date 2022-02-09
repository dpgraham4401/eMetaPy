import unittest
import os
import sys
import emeta
import dotenv


class MyTestCase(unittest.TestCase):

    def test_auth(self):
        if os.path.exists("C:\\Users\\dgraha01\\.env"):
            dotenv.load_dotenv("C:\\Users\\dgraha01\\.env")
        else:
            print("nope")
            sys.exit(1)
            emeta.authenticate()
        self.assertEqual(type(os.getenv('META_TOKEN')), str)

    def test_get_query(self):
        resp = emeta.get_query('2944', 'json')
        self.assertEqual(type(resp), list)

    def test_query_parameters(self):
        parameter = {"GEN_ID_VAR": "TXR000040923"}
        resp = emeta.get_query('2944', 'json', parameter)
        print(resp)
        self.assertEqual(type(resp), list)

    def test_multi_param_query(self):
        parameter = {"GEN_ID_VAR": "TXR000040923",
                     "TSDF_ID_VAR": "TXD000719518"}
        resp = emeta.get_query('2944', 'json', parameter)
        self.assertIn("Count of manifests", str(resp[0]))


if __name__ == '__main__':
    unittest.main()
