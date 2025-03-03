#!/usr/bin/env python3
"""
DataHandler module for handling data storage and retrieval.
"""

import os
import pandas as pd
from loguru import logger

class DataHandler:
    def __init__(self, filename="/app/data/jobs.csv"):
        self.filename = filename
        self.df = pd.DataFrame()

    def save_data(self, new_jobs):
        """Save scraped data to CSV."""
        try:
            # Initialize combined with new_jobs
            combined = new_jobs

            if os.path.exists(self.filename):
                try:
                    existing_df = pd.read_csv(self.filename)
                    if not existing_df.empty:
                        combined = pd.concat([existing_df, new_jobs]).drop_duplicates(subset=['title', 'link'])
                except Exception as e:
                    logger.warning(f"Could not read existing file: {str(e)}")

            # Ensure the data directory exists
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            # Save the combined dataframe
            combined.to_csv(self.filename, index=False)
            logger.info(f"{len(new_jobs)} new offers saved")

        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")

    def load_data(self):
        """Load previously saved data from CSV."""
        try:
            if os.path.exists(self.filename):
                self.df = pd.read_csv(self.filename)

                if self.df.empty:
                    return pd.DataFrame()
                else:
                    return self.df
            else:
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()
