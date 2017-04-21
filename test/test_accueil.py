import unittest 
import flask

app = flask.Flask(__name__)
# To run tests
# cd project_directory
# python -m unittest discover

class MyTestClass(unittest.TestCase): 

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass 

        # clean up logic for the test suite declared in the test module
        # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass 

        # initialization logic
        # code that is executed before each test
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 


        # clean up logic
        # code that is executed after each test
    def tearDown(self):
        pass 

        # test method
    # def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        # result = self.app.get('/') 

        # assert the status code of the response
        # self.assertEqual(result.status_code, 200) 

    # def test_home_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        # result = self.app.get('/') 

        # assert the response data
        # self.assertEqual(result.data, "Hello World!!!")

    def test_equal_numbers(self):
        self.assertEqual(2, 2) 

    # runs the unit tests in the module
    if __name__ == '__main__':
        unittest.main()
