#!/usr/bin/env python3
"""
Web interface for displaying scraped job listings and running the scraper.
"""

from flask import Flask, render_template, redirect, url_for, flash, jsonify
import os
import pandas as pd
import subprocess
import shutil
from datetime import datetime
from src.core.data_handler import DataHandler
from src.core.scraper import JobScraper

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'kelio-scraper-secret-key')

# Support both local development and deployment environments
csv_path = os.getenv('JOBS_CSV_PATH', 'data/jobs.csv')
data_handler = DataHandler(csv_path)

@app.route('/')
def index():
    """Display all scraped jobs."""
    jobs = data_handler.load_data()
    
    # If DataFrame is empty, return empty list
    if jobs.empty:
        return render_template('index.html', jobs=[], now=datetime.now())
    
    # Sort jobs by date (newest first) if date column exists
    if 'date' in jobs.columns:
        jobs = jobs.sort_values(by='date', ascending=False)
    
    # Convert DataFrame to list of dictionaries
    jobs_list = jobs.to_dict('records')
    
    return render_template('index.html', jobs=jobs_list, now=datetime.now())

@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    """Run the scraper to fetch new job listings."""
    try:
        # Create a scraper instance and run it
        scraper = JobScraper()
        scraper.run()
        
        # Get the number of new jobs found
        new_jobs_count = len(scraper.new_jobs)
        
        # Return success message with job count information
        if new_jobs_count > 0:
            return jsonify({
                'success': True,
                'message': f'Le scraper a trouvé {new_jobs_count} offre(s) d\'emploi.'
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Le scraper a été exécuté avec succès. Aucune nouvelle offre trouvée.'
            })
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"Scraper error: {str(e)}")
        print(traceback.format_exc())
        
        # Return error message
        return jsonify({
            'success': False,
            'message': f'Erreur lors de l\'exécution du scraper: {str(e)}'
        }), 500

@app.route('/clear-jobs', methods=['POST'])
def clear_jobs():
    """Clear all saved job listings."""
    try:
        # Create an empty DataFrame with the same columns as the original
        empty_df = pd.DataFrame(columns=['title', 'link', 'company', 'location', 'date'])
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Save the empty DataFrame to the CSV file
        empty_df.to_csv(csv_path, index=False)
        
        # Update the data_handler's DataFrame
        data_handler.df = empty_df
        
        # Return success message
        return jsonify({
            'success': True,
            'message': 'Toutes les offres d\'emploi ont été supprimées.'
        })
    except Exception as e:
        # Return error message
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la suppression des offres: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('src/templates', exist_ok=True)
    
    # Get port from environment variable (for cloud deployment)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('APP_DEBUG', 'False').lower() == 'true'
    
    app.run(debug=debug, host='0.0.0.0', port=port)