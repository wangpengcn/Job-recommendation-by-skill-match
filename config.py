# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:26:22 2018

@author: Peng Wang
"""
# Saved file for each job url
JOBS_LINKS_JSON_FILE = r'./data/indeed_jobs_links.json'
# Saved file for each job info
JOBS_INFO_JSON_FILE = r'./data/indeed_jobs_info.json'
# Saved file for recommended jobs
RECOMMENDED_JOBS_FILE = r'./data/recommended_jobs'
# Path to webdriver exe
WEBDRIVER_PATH = r'D:\chromedriver\chromedriver.exe'
# Cities to search: 6 largest Canadian cities
JOB_LOCATIONS = ['Vancouver,BC', 'Toronto,ON', 'Montréal,QC', 'Ottawa,ON', 'Calgary,AB', 'Edmonton,AB']
# Seach "data scientist" OR "data+engineer" OR "data+analyst" with quotation marks
JOB_SEARCH_WORDS = '"data scientist"+OR+"data engineer"+OR+"data analyst"'
# To avoid same job posted multiple times, we only look back for 30 days
DAY_RANGE = 30
# Path to sample resume
SAMPLE_RESUME_PDF = r'./data/PWang_resume.pdf'
