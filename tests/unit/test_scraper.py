import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from bs4 import BeautifulSoup
# Importez les classes/fonctions à tester
from src.core.scraper import JobScraper
from src.core.data_handler import DataHandler
from src.core.notifier import Notifier

class TestJobScraper(unittest.TestCase):

    def setUp(self):
        """Setup method to create a JobScraper instance before each test."""
        self.scraper = JobScraper()
        # Mock the config, as we don't want to load the real one in unit tests
        self.scraper.config = {
            'scraping': {
                'url': 'mock_url',
                'keywords': ['test_keyword']
            },
            'email': {'enabled': False}  # Disable email sending for tests
        }

    @patch('src.core.scraper.requests.get')
    def test_fetch_html_success(self, mock_get):
        """Test successful HTML fetching."""
        mock_response = MagicMock()
        mock_response.text = "<html><body>Mock HTML</body></html>"
        mock_response.raise_for_status.return_value = None  # Simulate no HTTP errors
        mock_get.return_value = mock_response

        html = self.scraper.fetch_html()
        self.assertEqual(html, "<html><body>Mock HTML</body></html>")
        mock_get.assert_called_once_with('mock_url', headers=unittest.mock.ANY, timeout=10)

    @patch('src.core.scraper.requests.get')
    def test_fetch_html_failure(self, mock_get):
        """Test HTML fetching failure and fallback to Selenium."""
        mock_get.side_effect = Exception("Simulated request failure")

        # Mock Selenium behavior
        with patch('src.core.scraper.webdriver.Chrome') as MockChrome:
            mock_driver = MagicMock()
            mock_driver.page_source = "<html><body>Mock Selenium HTML</body></html>"
            MockChrome.return_value = mock_driver

            html = self.scraper.fetch_html()
            self.assertEqual(html, "<html><body>Mock Selenium HTML</body></html>")
            # Assert that Selenium was used
            MockChrome.assert_called_once()
            mock_driver.get.assert_called_once_with('mock_url')
            mock_driver.quit.assert_called_once()

    def test_parse_jobs(self):
        """Test parsing of job offers from HTML."""
        # Create a sample HTML snippet
        html = """
        <div class="offer">
            <h2 class="title">Job Title with test_keyword</h2>
            <a href="/job1">Link</a>
        </div>
        <div class="offer">
            <h3 class="job-title">Another Job</h3>
            <a href="/job2">Link</a>
        </div>
        <div class="offer">
            <h2 class="title">Job with Test_Keyword</h2>
            <a href="https://example.com/job3">Link</a>
        </div>
        <div class="other-div">Not a job offer</div>
        """
        expected_jobs = pd.DataFrame([
            {'title': 'Job Title with test_keyword', 'link': 'https://www.bodet.com/job1', 'company': 'Kelio', 'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')},
            {'title': 'Job with Test_Keyword', 'link': 'https://example.com/job3', 'company': 'Kelio', 'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')},
        ])

        actual_jobs = self.scraper.parse_jobs(html)
        pd.testing.assert_frame_equal(actual_jobs.reset_index(drop=True), expected_jobs.reset_index(drop=True), check_dtype=False) #reset index, sometime the test fail because of index

    def test_parse_jobs_empty(self):
        """Test parsing when there are no job offers."""
        html = "<div class='other-div'>No job offers</div>"
        actual_jobs = self.scraper.parse_jobs(html)
        self.assertTrue(actual_jobs.empty)

    @patch('src.core.scraper.Notifier.send_email')
    @patch('src.core.scraper.DataHandler.save_data')
    def test_run(self, mock_save_data, mock_send_email):
        """Test the main run method."""
        # Mock fetch_html and parse_jobs
        self.scraper.fetch_html = MagicMock(return_value="mock_html")
        self.scraper.parse_jobs = MagicMock(return_value=pd.DataFrame([{'title': 'Test Job', 'link': 'test_link'}]))

        self.scraper.run()

        self.scraper.fetch_html.assert_called_once()
        self.scraper.parse_jobs.assert_called_once_with("mock_html")
        mock_save_data.assert_called_once()
        mock_send_email.assert_called_once()

    @patch('src.core.scraper.Notifier.send_email')
    @patch('src.core.scraper.DataHandler.save_data')
    def test_run_no_new_jobs(self, mock_save_data, mock_send_email):
        """Test run method when no new jobs are found."""
        self.scraper.fetch_html = MagicMock(return_value="mock_html")
        self.scraper.parse_jobs = MagicMock(return_value=pd.DataFrame())  # Return empty DataFrame

        self.scraper.run()

        self.scraper.fetch_html.assert_called_once()
        self.scraper.parse_jobs.assert_called_once_with("mock_html")
        mock_save_data.assert_not_called()  # Should not save
        mock_send_email.assert_not_called() # Should not send email

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.data_handler = DataHandler(filename='test_jobs.csv')

    def tearDown(self):
        # Clean up the test file after each test
        import os
        if os.path.exists('test_jobs.csv'):
            os.remove('test_jobs.csv')

    def test_save_and_load_data(self):
        new_jobs = pd.DataFrame([
            {'title': 'Job 1', 'link': 'link1'},
            {'title': 'Job 2', 'link': 'link2'}
        ])

        self.data_handler.save_data(new_jobs)
        loaded_jobs = self.data_handler.load_data()
        pd.testing.assert_frame_equal(loaded_jobs, new_jobs)

    def test_save_data_append(self):
        # First save
        initial_jobs = pd.DataFrame([{'title': 'Job 1', 'link': 'link1'}])
        self.data_handler.save_data(initial_jobs)

        # Then save new data
        new_jobs = pd.DataFrame([{'title': 'Job 2', 'link': 'link2'}])
        self.data_handler.save_data(new_jobs)

        # Load and check
        loaded_jobs = self.data_handler.load_data()
        expected_jobs = pd.DataFrame([
            {'title': 'Job 1', 'link': 'link1'},
            {'title': 'Job 2', 'link': 'link2'}
        ])
        pd.testing.assert_frame_equal(loaded_jobs.reset_index(drop=True), expected_jobs.reset_index(drop=True))

    def test_save_data_duplicates(self):
        # First save
        initial_jobs = pd.DataFrame([{'title': 'Job 1', 'link': 'link1'}])
        self.data_handler.save_data(initial_jobs)

        # Save duplicate data
        duplicate_jobs = pd.DataFrame([{'title': 'Job 1', 'link': 'link1'}])
        self.data_handler.save_data(duplicate_jobs)

        loaded_jobs = self.data_handler.load_data()
        expected_jobs = pd.DataFrame([{'title': 'Job 1', 'link': 'link1'}])

        pd.testing.assert_frame_equal(loaded_jobs.reset_index(drop=True), expected_jobs.reset_index(drop=True))

class TestNotifier(unittest.TestCase):
    def setUp(self):
        self.notifier = Notifier()

    @patch('src.core.notifier.smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        """Test email sending functionality."""
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        self.notifier.send_email("Test Subject", "Test Body")

        mock_smtp.assert_called_once_with('smtp.example.com', 587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
        mock_smtp_instance.send_message.assert_called_once()

    @patch('src.core.notifier.smtplib.SMTP')
    def test_send_email_disabled(self, mock_smtp):
        """Test email sending when disabled in config."""
        self.notifier.config['email']['enabled'] = False
        self.notifier.send_email("Test Subject", "Test Body")
        mock_smtp.assert_not_called()

if __name__ == '__main__':
    unittest.main() 