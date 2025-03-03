import unittest
import os
import pandas as pd
from src.core.scraper import JobScraper
from src.core.data_handler import DataHandler
from unittest.mock import patch, MagicMock

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """Setup method to prepare for integration tests."""
        self.test_csv_path = 'test_integration_jobs.csv'
        # Create a JobScraper instance
        self.scraper = JobScraper()
        # Override the config to use test settings
        self.scraper.config = {
            'scraping': {
                'url': 'file://' + os.path.abspath('tests/integration/test_page.html'),  # Use a local HTML file
                'keywords': ['keyword1', 'keyword2']
            },
            'email': {
                'enabled': False,  # Disable email for integration tests
                'receiver': 'test@example.com',
                'smtp_server': 'smtp.example.com',
                'smtp_port': 587
            }
        }
        self.scraper.data_handler.filename = self.test_csv_path

    def tearDown(self):
        """Teardown method to clean up after tests."""
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

    def test_full_scraping_process(self):
        """Test the entire scraping process from fetching to saving."""

        # Create a test HTML file
        with open('tests/integration/test_page.html', 'w') as f:
            f.write("""
            <div class="offer">
                <h2 class="title">Job with keyword1</h2>
                <a href="/job1">Link</a>
            </div>
            <div class="offer">
                <h3 class="title">Job with keyword2</h3>
                <a href="/job2">Link</a>
            </div>
            <div class="offer">
                <h2 class="title">No keyword here</h2>
                <a href="/job3">Link</a>
            </div>
            """)

        # Run the scraper
        self.scraper.run()

        # Check if the CSV file was created and contains the expected data
        self.assertTrue(os.path.exists(self.test_csv_path))
        df = pd.read_csv(self.test_csv_path)
        self.assertEqual(len(df), 2)
        self.assertIn('Job with keyword1', df['title'].tolist())
        self.assertIn('Job with keyword2', df['title'].tolist())
        self.assertIn('https://www.bodet.com/job1', df['link'].tolist())
        self.assertIn('https://www.bodet.com/job2', df['link'].tolist())

    @patch('src.core.notifier.Notifier.send_email')
    def test_full_scraping_process_with_email(self, mock_send_email):
        """Test with email sending mocked."""
        self.scraper.config['email']['enabled'] = True # Enable email

        with open('tests/integration/test_page.html', 'w') as f:
            f.write("""
            <div class="offer">
                <h2 class="title">Job with keyword1</h2>
                <a href="/job1">Link</a>
            </div>""")

        self.scraper.run()
        self.assertTrue(os.path.exists(self.test_csv_path))
        mock_send_email.assert_called_once()


if __name__ == '__main__':
    unittest.main() 