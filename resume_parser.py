import os
import json
import re
import spacy
import nltk
import pandas as pd
from typing import Dict, List, Any

class ResumeParser:
    def __init__(self):
        # Download necessary NLTK resources
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        
        # Load spaCy language model
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("spaCy language model loaded successfully!")
        except OSError:
            print("Downloading spaCy language model...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            print("spaCy language model downloaded and loaded successfully!")

    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Main method to parse resume text into structured JSON
        """
        parsed_data = {
            "personal_info": self._extract_personal_info(resume_text),
            "skills": self._extract_skills(resume_text),
            "work_experience": self._extract_work_experience(resume_text),
            "education": self._extract_education(resume_text),
            "projects": self._extract_projects(resume_text),
            "certifications": self._extract_certifications(resume_text)
        }
        return parsed_data

    def _extract_personal_info(self, resume_text: str) -> Dict[str, str]:
        """
        Extract personal information from resume 
        """
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, resume_text)
        # Phone number extraction (flexible format)
        phone_pattern = r'(\+?\d{1,3})?[-\s.]?(\d{3})[-\s.]?(\d{3})[-\s.]?(\d{4})'
        phone_match = re.search(phone_pattern, resume_text)
        if phone_match:
            phones = ''.join(phone_match.groups())
        else:
            phones = None
        # Name extraction (using spaCy)
        doc = self.nlp(resume_text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        return {
            "name": names[0] if names else None,
            "email": emails[0] if emails else None,
            "phone": phones,
            "location": self._extract_location(resume_text)
            }

    def _extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract technical and soft skills from resume
        """
        # Predefined skill keywords
        tech_skills = [
            'python', 'java', 'machine learning', 'ai', 'tensorflow', 
            'pytorch', 'javascript', 'react', 'sql', 'git'
        ]
        
        # Case-insensitive skill extraction
        found_skills = [
            skill for skill in tech_skills 
            if skill.lower() in resume_text.lower()
        ]
        
        return list(set(found_skills))

    def _extract_work_experience(self, resume_text: str) -> List[Dict[str, str]]:
        """
        Extract work experience details
        """
        # Simple regex to find job titles and companies
        job_pattern = r'(.*?)\s*\|\s*(.*?)\s*\|\s*([A-Za-z]+\s+\d{4}\s*-\s*[A-Za-z]+\s+\d{4})'
        experiences = re.findall(job_pattern, resume_text, re.MULTILINE)
        
        return [
            {
                "job_title": exp[0].strip(),
                "company": exp[1].strip(),
                "duration": exp[2].strip()
            } for exp in experiences
        ]

    def _extract_education(self, resume_text: str) -> List[Dict[str, str]]:
        """
        Extract education details
        """
        # Regex to find degree and institution
        edu_pattern = r'(.*?)\s*\|\s*(.*)'
        educations = re.findall(edu_pattern, resume_text, re.MULTILINE)
        
        return [
            {
                "degree": edu[0].strip(),
                "institution": edu[1].strip()
            } for edu in educations
        ]

    def _extract_projects(self, resume_text: str) -> List[Dict[str, str]]:
        """
        Extract project details
        """
        # Simple project extraction based on specific sections
        project_section = re.findall(r'Project.*?\n(.*?)(?=\n\n|\n#)', resume_text, re.DOTALL)
        
        if project_section:
            project_pattern = r'### (.*?)\n(.*?)(?=\n###|\n$)'
            projects = re.findall(project_pattern, project_section[0], re.DOTALL)
            
            return [
                {
                    "name": proj[0].strip(),
                    "description": proj[1].strip().replace('\n', ' ')
                } for proj in projects
            ]
        return []

    def _extract_certifications(self, resume_text: str) -> List[str]:
        """
        Extract certifications
        """
        # Simple certification extraction
        cert_pattern = r'- (.*?Certified.*)'
        certifications = re.findall(cert_pattern, resume_text)
        return certifications
   
    def _extract_location(self, resume_text: str) -> str:
        """
        Extract location from the first line
        Expected format: Name | Location | Phone | Email
        """
        lines = resume_text.strip().split('\n')
        if lines:
            parts = [p.strip() for p in lines[0].split('|')]
            if len(parts) >= 2:
                return parts[1]  # Assuming second item is location
            return None


def main():
    # Example usage
    with open('resume.md', 'r') as file:
        resume_text = file.read()
    
    parser = ResumeParser()
    parsed_resume = parser.parse_resume(resume_text)
    
    # Save to JSON file
    with open('parsed_resume.json', 'w') as outfile:
        json.dump(parsed_resume, outfile, indent=2)
    
    print("Resume parsed successfully!")

if __name__ == "__main__":
    main()