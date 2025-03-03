"""
Core package for the Kelio Scraper application.
This package contains the main components for scraping, data handling, and notifications.
"""

# Version du package
__version__ = '0.1.0'

# Expose core modules
from src.core.scraper import JobScraper
from src.core.data_handler import DataHandler
from src.core.notifier import Notifier
from src.core.ai_formatter import AIFormatter