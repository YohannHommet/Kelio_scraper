from loguru import logger
import os
import pandas as pd
from typing import List, Dict
import requests
import json

class AIFormatter:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        
    def format_jobs(self, jobs: pd.DataFrame) -> str:
        """Format job listings using AI to create a more readable email content"""
        if jobs.empty:
            return ""
            
        # Convert jobs to a list of dictionaries for easier formatting
        jobs_list = jobs.to_dict('records')
        
        try:
            logger.debug("Making API call to Groq...")
            formatted_content = self._format_with_ai(jobs_list)
            logger.info("AI successfully formatted the job listings")
            return formatted_content
            
        except Exception as e:
            logger.error(f"Error while formatting jobs with Groq API: {str(e)}")
            logger.debug(f"Error details: {e.__class__.__name__}")
            logger.info("Falling back to basic formatting")
            return self._basic_format(jobs_list)
    
    def _prepare_jobs_text(self, jobs: List[Dict]) -> str:
        """Convert job listings to a formatted text string"""
        return "\n\n".join([
            f"Title: {job['title']}\n"
            f"Company: {job['company']}\n"
            f"Location: {job['location']}\n"
            f"Link: {job['link']}"
            for job in jobs
        ])
    
    def _format_with_ai(self, jobs: List[Dict]) -> str:
        """Format job listings using the Groq AI API"""
        jobs_text = self._prepare_jobs_text(jobs)
        
        system_message = (
            "You are an expert email content designer specializing in job listings. Your mission is to transform raw job data into a visually appealing, scannable HTML email that recipients will be excited to open and read in common email clients like Outlook and Gmail. Follow these guidelines:\n\n"
            "1. CREATE HTML EMAIL CONTENT:\n"
            "   - Generate valid, clean HTML that will render properly in all email clients\n"
            "   - Use basic HTML tags like <div>, <p>, <h2>, <h3>, <br>, <strong>, <ul>, <li>, <a>, etc.\n"
            "   - Include proper DOCTYPE and HTML structure with <html>, <head>, and <body> tags\n"
            "   - Add inline CSS for styling (no external stylesheets or <style> tags as they may be stripped)\n"
            "   - Use table-based layouts for structure as they're most reliable in email clients\n\n"
            "2. EMAIL-SAFE HTML DESIGN:\n"
            "   - Use a single-column layout with a width of 600px maximum\n"
            "   - Set font-family to web-safe fonts like Arial, Helvetica, sans-serif\n"
            "   - Use inline CSS for all styling (style=\"property: value;\")\n"
            "   - Avoid CSS properties that aren't widely supported in email clients\n"
            "   - Use HTML tables for layout structure when needed\n\n"
            "3. CONTENT ORGANIZATION:\n"
            "   - Group jobs by location with clear section headers\n"
            "   - Make job titles stand out with larger font size or bold formatting\n"
            "   - Include relevant emojis where appropriate\n"
            "   - Create visual separation between job listings using borders or background colors\n"
            "   - Make links clearly visible and ensure they're properly formatted as HTML <a> tags\n\n"
            "4. EXAMPLE HTML STRUCTURE:\n"
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            "    <meta charset=\"UTF-8\">\n"
            "    <title>New Job Listings</title>\n"
            "</head>\n"
            "<body style=\"font-family: Arial, Helvetica, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;\">\n"
            "    <h1 style=\"color: #333; text-align: center;\">New Job Listings</h1>\n"
            "    \n"
            "    <div style=\"margin-bottom: 30px;\">\n"
            "        <h2 style=\"background-color: #f0f0f0; padding: 10px; border-radius: 5px;\">📍 Location Name</h2>\n"
            "        \n"
            "        <div style=\"border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px;\">\n"
            "            <h3 style=\"margin-top: 0; color: #2a5885;\">📋 Job Title</h3>\n"
            "            <p style=\"margin: 5px 0;\">🏢 Company Name</p>\n"
            "            <p style=\"margin: 5px 0;\">📍 Location</p>\n"
            "            <p style=\"margin: 5px 0;\"><a href=\"https://job-link.com\" style=\"color: #0066cc;\">🔗 Apply Here</a></p>\n"
            "        </div>\n"
            "        \n"
            "        <!-- Additional job listings for this location -->\n"
            "    </div>\n"
            "    \n"
            "    <!-- Additional location sections -->\n"
            "</body>\n"
            "</html>\n\n"
            "IMPORTANT: Your output must be complete, valid HTML that will render correctly in email clients. Include all necessary HTML tags and inline CSS styling. Make sure all links are properly formatted as HTML <a> tags."
        )
        
        user_prompt = f"Please format these new job listings into an HTML email that will display correctly in email clients. Group jobs by location and make the content visually appealing and easy to scan:\n\n{jobs_text}"
        
        logger.debug(f"Sending prompt to Groq API:\n{user_prompt}")
        
        content = self._call_groq(system_message, user_prompt)
        
        # Clean the content to remove any backticks or code block markers
        cleaned_content = self._clean_html_content(content)
        logger.debug(f"Cleaned content:\n{cleaned_content}")
        
        return cleaned_content
    
    def _clean_html_content(self, content: str) -> str:
        """
        Clean the HTML content by removing backticks and code block markers.
        """
        # Remove opening code block markers like ```html, ```HTML, etc.
        content = content.strip()
        if content.startswith("```"):
            # Find the first newline to remove the entire first line with backticks
            first_newline = content.find("\n")
            if first_newline != -1:
                content = content[first_newline + 1:]
        
        # Remove closing backticks
        if content.endswith("```"):
            content = content[:-3].strip()
        
        # Remove any other backtick sequences that might be present
        if "```" in content:
            logger.warning("Found additional backtick sequences in the content, attempting to clean")
            lines = content.split("\n")
            cleaned_lines = [line for line in lines if not line.strip() == "```"]
            content = "\n".join(cleaned_lines)
        
        return content
    
    def _basic_format(self, jobs: List[Dict]) -> str:
        """Fallback basic formatting if AI fails"""
        html_content = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <title>New Job Listings</title>',
            '</head>',
            '<body style="font-family: Arial, Helvetica, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">',
            '    <h1 style="color: #333; text-align: center;">New Job Listings</h1>'
        ]
        
        # Group jobs by location
        locations = {}
        for job in jobs:
            location = job['location']
            if location not in locations:
                locations[location] = []
            locations[location].append(job)
        
        # Generate HTML for each location group
        for location, location_jobs in locations.items():
            html_content.append(f'    <div style="margin-bottom: 30px;">')
            html_content.append(f'        <h2 style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">📍 {location}</h2>')
            
            for job in location_jobs:
                html_content.append(f'        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px;">')
                html_content.append(f'            <h3 style="margin-top: 0; color: #2a5885;">📋 {job["title"]}</h3>')
                html_content.append(f'            <p style="margin: 5px 0;">🏢 {job["company"]}</p>')
                html_content.append(f'            <p style="margin: 5px 0;">📍 {job["location"]}</p>')
                html_content.append(f'            <p style="margin: 5px 0;"><a href="{job["link"]}" style="color: #0066cc;">🔗 Apply Here</a></p>')
                html_content.append(f'        </div>')
            
            html_content.append(f'    </div>')
        
        html_content.append('</body>')
        html_content.append('</html>')
        
        return '\n'.join(html_content)

    def _call_groq(self, system_message: str, user_prompt: str) -> str:
        """
        Call the Groq API and return the formatted content.
        """
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "model": self.model,
            "temperature": 0.7,
            "max_completion_tokens": 4096,
            "top_p": 0.95,
            "stream": False,
            "stop": None
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.groq_api_key}"
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

        result = response.json()
        return result["choices"][0]["message"]["content"] 