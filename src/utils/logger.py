#!/usr/bin/env python3
"""
Logger module to setup application logging.
"""

import logging


def setup_logger(name='scraper_logger', level=logging.DEBUG):
    """Setup and return a configured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
