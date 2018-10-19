# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:35:00 2018

@author: Peng Wang

Build a simple data-science-skill-keyword-based job recommendation engine, 
which match keywords from resume to data science jobs in major Canadian cities.
Step 1: Scrape "data scientist/engineer/analyst" jobs from indeed.ca
Step 2: Tokenize and extract skill keywords from job descriptions
Step 3: Tokenize and extract skill keywords from resume
Step 4: Calculate Jaccard similarity of keywords from posted jobs and resume, 
        and recommend top 5 matches 
"""
import sys 
import config, web_scrapper
from skill_keyword_match import skill_keyword_match

def main():
    # If city included, only search and recommend jobs in the city
    location = ''
    if (len(sys.argv) > 1):
        # Check if input city name matches our pre-defined list
        if (sys.argv[1] in config.JOB_LOCATIONS):
            location = sys.argv[1]
        else:
            sys.exit('*** Please try again. *** \nEither leave it blank or input a city from this list:\n{}'.format('\n'.join(config.JOB_LOCATIONS)))
    # ---------------------------------------------------
    # ---- Scrape from web or read from local saved -----
    # ---------------------------------------------------
    jobs_info = web_scrapper.get_jobs_info(location)    
    # ---------------------------------------------------
    # -------- Keyword extraction and analysis ----------
    # ---------------------------------------------------
    # Initialize skill_keyword_match with job_info
    skill_match = skill_keyword_match(jobs_info)
    # Extract skill keywords from job descriptions 
    skill_match.extract_jobs_keywords()
    # Show exploratory data analysis if job search is nationwide i.e. no input for city
    if (len(sys.argv) == 1):
        skill_match.exploratory_data_analysis()
    # ---------------------------------------------------
    # -- Job recommendation based on skill matching -----
    # ---------------------------------------------------
    resume_skills = skill_match.extract_resume_keywords(config.SAMPLE_RESUME_PDF)
    # Calculate similarity of skills from a resume and job posts 
    top_job_matches = skill_match.cal_similarity(resume_skills.index, location)
    # Save matched jobs to a file
    top_job_matches.to_csv(config.RECOMMENDED_JOBS_FILE+location+'.csv', index=False)
    print('File of recommended jobs saved')
     
if __name__ == "__main__": 
    main()
    
    