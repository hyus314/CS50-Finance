# test_app.py
import unittest
from app import app

class FlaskTest(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()

    def test_home_status_code(self):
        # Test the status code of the home route
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
