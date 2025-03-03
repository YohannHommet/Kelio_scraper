#!/usr/bin/env python3
"""
Notifier module for sending notifications using Resend API.
"""

import os
import json
import subprocess
from loguru import logger

class Notifier:
    def __init__(self):
        self.resend_api_key = os.getenv('RESEND_API_KEY')
        self.sender = os.getenv('EMAIL_SENDER', 'onboarding@resend.dev')
        self.receiver = os.getenv('EMAIL_RECEIVER')

    def send_email(self, subject, body):
        """Send an email notification using Resend API."""
        if not os.getenv('SEND_EMAIL', 'False').lower() == 'true':
            return

        try:
            data = {
                "from": self.sender,
                "to": self.receiver,
                "subject": subject,
                "html": body  # Assuming body is already in HTML format from AI formatter
            }

            curl_command = [
                "curl",
                "-X", "POST",
                "https://api.resend.com/emails",
                "-H", f"Authorization: Bearer {self.resend_api_key}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(data)
            ]

            result = subprocess.run(curl_command, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Curl call failed: {result.stderr}")

            logger.info("Email sent successfully via Resend")
            logger.debug(f"Resend API response: {result.stdout}")

        except Exception as e:
            logger.error(f"Email error: {str(e)}")

    def send_notification(self, message):
        """Send a notification with the provided message."""
        self.send_email("[Kelio Scraper] Notification", message)
