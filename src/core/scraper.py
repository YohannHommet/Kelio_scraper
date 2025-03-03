#!/usr/bin/env python3
"""
Main scraper module.
This module orchestrates the scraping process.
"""

import os
import re
import yaml
import requests
import pandas as pd
from time import sleep
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from loguru import logger
from tenacity import retry, wait_exponential, stop_after_attempt
from src.core.notifier import Notifier
from src.core.data_handler import DataHandler
from src.core.ai_formatter import AIFormatter

# Configuration initiale
load_dotenv()
logger.add("/app/logs/scraper.log", rotation="1 week")

class JobScraper:
    def __init__(self):
        self.data_handler = DataHandler()
        self.notifier = Notifier()
        self.ai_formatter = AIFormatter()
        self.new_jobs = pd.DataFrame()

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
    def fetch_html(self):
        try:
            logger.info(f"Fetching HTML from URL: {os.getenv('SCRAPER_URL')}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            response = requests.get(os.getenv('SCRAPER_URL'), headers=headers, timeout=15)
            response.raise_for_status()

            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response content type: {response.headers.get('Content-Type', 'unknown')}")
            
            if 'offres-d-emploi' in response.text or 'contentpane' in response.text:
                logger.debug("Valid job page content found")
                return response.text
            
            logger.warning("Invalid page content - no jobs section found")
            logger.debug(f"Response content preview: {response.text[:500]}...")
            raise Exception('Contenu invalide - section des offres d\'emploi non trouvée')

        except Exception as e:
            logger.warning(f"Fallback to Selenium: {str(e)}")
            try:
                options = Options()
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                
                logger.info("Initializing Selenium WebDriver")
                driver = webdriver.Chrome(options=options)
                
                logger.info(f"Navigating to URL: {os.getenv('SCRAPER_URL')}")
                driver.get(os.getenv('SCRAPER_URL'))
                
                logger.info("Waiting for page to load...")
                sleep(5)  # Increased wait time
                
                logger.debug(f"Page title: {driver.title}")
                html = driver.page_source
                
                logger.debug(f"Selenium HTML content length: {len(html)} characters")
                driver.quit()
                
                return html
            except Exception as selenium_error:
                logger.error(f"Selenium error: {str(selenium_error)}")
                raise Exception(f"Failed to fetch HTML with both methods: {str(e)} and Selenium error: {str(selenium_error)}")

    def parse_jobs(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        
        logger.debug(f"HTML content length: {len(html)} characters")
        all_jobs = soup.find_all('tr', class_=['sectiontableentry1', 'sectiontableentry2'])
        logger.debug(f"Total jobs found on page: {len(all_jobs)}")
        
        # Log the first few characters of HTML for debugging
        logger.debug(f"HTML preview: {html[:500]}...")
        
        if len(all_jobs) == 0:
            logger.warning("No job entries found in the HTML. Check the page structure or selectors.")
            # Try alternative selectors if the primary ones don't work
            all_jobs = soup.select('table.contentpane tr')
            logger.debug(f"Trying alternative selector, found: {len(all_jobs)} jobs")
        
        for item in all_jobs:
            try:
                cells = item.find_all('td')
                
                # Skip if not enough cells
                if len(cells) < 4:
                    logger.debug(f"Skipping row with insufficient cells: {len(cells)}")
                    continue
                
                # Check if the first cell has a link
                title_link = cells[0].find('a')
                if not title_link:
                    logger.debug("Skipping row without title link")
                    continue
                
                title = title_link.get_text(strip=True)
                link = title_link['href']
                company = cells[1].get_text(strip=True)
                location = cells[3].get_text(strip=True)
                
                if not link.startswith('http'):
                    link = f"https://www.bodet.com{link}"

                keywords = ['dev', 'développeur', 'developpeur', 'développement', 'angular', 'vue', 'vue js', 'vue.js', 'nodejs', 'javascript', 'js', 'php', 'symfony', 'frontend', 'front-end', 'front', 'back-end', 'backend', 'back', 'fullstack', 'full-stack', 'full stack']
                locations = ['cholet', 'trémentines', 'angers']

                # Log each job for debugging
                logger.debug(f"Found job: {title} at {location}")
                
                if any(kw.lower() in title.lower() for kw in keywords) and location.lower() in locations:
                    jobs.append({
                        'title': title,
                        'link': link,
                        'company': company,
                        'location': location,
                        'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
                    })
                    logger.debug(f"Added matching job: {title} at {location}")
                    
            except Exception as e:
                logger.error(f"Erreur parsing: {str(e)}")
        
        logger.info(f"Total jobs found: {len(jobs)}")
        return pd.DataFrame(jobs)

    def run(self):
        try:
            logger.info("Starting scraping...")

            # Charger les offres existantes
            existing_jobs = self.data_handler.load_data()
            existing_titles = set(existing_jobs['title']) if not existing_jobs.empty else set()

            html = self.fetch_html()
            self.new_jobs = self.parse_jobs(html)
            
            # Filtrer pour ne garder que les nouvelles offres
            if not self.new_jobs.empty:
                really_new_jobs = self.new_jobs[~self.new_jobs['title'].isin(existing_titles)]
                
                if not really_new_jobs.empty:
                    self.data_handler.save_data(really_new_jobs)
                    
                    # Utiliser l'IA pour formater le contenu de l'email
                    body = self.ai_formatter.format_jobs(really_new_jobs)
                    
                    if os.getenv('SEND_EMAIL'):
                        self.notifier.send_email(
                            f"[Kelio] {len(really_new_jobs)} nouvelle(s) offre(s) de développeur",
                            body
                        )
                    logger.info(f"{len(really_new_jobs)} nouvelles offres trouvées")
                else:
                    logger.info("Aucune nouvelle offre trouvée")

            logger.success("Process completed")
        except Exception as e:
            logger.error(f"Critical error: {str(e)}")
            # Notification d'erreur
            self.notifier.send_notification(f"Erreur critique: {str(e)}")

if __name__ == "__main__":
    scraper = JobScraper()
    scraper.run()
