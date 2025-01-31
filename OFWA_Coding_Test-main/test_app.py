import unittest
from app import app
import data_analysis

class TestGalamsayAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_latest_analysis(self):
        response = self.app.get('/api/analysis')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('total_sites', data)
        self.assertIn('region_with_most_sites', data)
        self.assertIn('average_sites_per_region', data)
        self.assertIn('timestamp', data)

    def test_get_analysis_history(self):
        response = self.app.get('/api/analysis/history')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn('total_sites', data[0])
            self.assertIn('region_with_most_sites', data[0])
            self.assertIn('average_sites_per_region', data[0])
            self.assertIn('timestamp', data[0])

    def test_get_raw_data(self):
        response = self.app.get('/api/data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn('city', data[0])
            self.assertIn('region', data[0])
            self.assertIn('number_of_sites', data[0])
            self.assertIn('timestamp', data[0])

class TestDataAnalysis(unittest.TestCase):
    def test_cities_exceeding_threshold(self):
        threshold = 10
        cities = data_analysis.cities_exceeding_threshold(threshold)
        self.assertIsInstance(cities, list)

if __name__ == '__main__':
    unittest.main() 