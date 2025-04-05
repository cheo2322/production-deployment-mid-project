import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_recommendations_endpoint(self):
        response = self.client.get('/recommendations/1?k_neighbors=5&top_n=20')
        self.assertEqual(response.status_code, 200) 
        self.assertIn('recommendations', response.json)

    def test_invalid_user(self):
        # Prueba con un usuario inexistente
        response = self.client.get('/recommendations/999?k_neighbors=5&top_n=20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('recommendations'), [])

if __name__ == '__main__':
    unittest.main()