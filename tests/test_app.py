import unittest
from app.app import create_app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_recommendations_endpoint(self):
        response = self.client.get('/recommendations/1?k_neighbors=5&top_n=20')
        self.assertEqual(response.status_code, 200)
        self.assertIn('recommendations', response.json)

    def test_invalid_user(self):
        response = self.client.get('/recommendations/999?k_neighbors=5&top_n=20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('recommendations'), [])
    
    def test_random_recommendations(self):
        response = self.client.get('/recommendations/random')
        
        self.assertEqual(response.status_code, 200)
        
        self.assertIn('user_id', response.json)
        self.assertIn('recommendations', response.json)
        
        self.assertIsInstance(response.json['recommendations'], list)
        self.assertGreater(len(response.json['recommendations']), 0, "Empty list.")

if __name__ == '__main__':
    unittest.main()