import os
import unittest

# set to null
CACHE_TYPE = "null"

from app import app, cache

class getDepedenciesTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        
        cache.init_app(app, config={'CACHE_TYPE': 'null'})
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass
    
    ###############
    #### tests ####
    ###############
    
    def test_get_depedencies_valid_queries(self):
        response = self.app.get('/dependencies', query_string={'package' : "express1", 'version' : "latest"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/dependencies', query_string={'package' : "express1", 'version' : "latest"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/dependencies', query_string={'version' : "latest"}, follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    def test_get_depedencies_invalid_queries(self):
        response = self.app.get('/dependencies', query_string={'package' : "80ruwNhjBGsbdDmrA8sPxGG7twxe2C4LkW2eq3kQ11", 'version' : "latest"}, 
                            follow_redirects=True)
        self.assertEqual(response.status_code, 422)

        response = self.app.get('/dependencies', query_string={'package' : "express1", 'version' : "gU4BIrIZRrgQ6KabQBElJIhSWtCT2bP13T6bnBIG1"}, 
                            follow_redirects=True)
        self.assertEqual(response.status_code, 422)

        response = self.app.get('/dependencies', query_string={'version' : "latest"}, follow_redirects=True)
        self.assertEqual(response.status_code, 422)
    
if __name__ == "__main__":
    unittest.main()