# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:52:03 2018

@author: Peng Wang

Tokenize text, extract keywords, and recommend jobs by matching keywords from resume with jobs
"""

import re
from nltk.corpus import stopwords
from collections import Counter 
import pandas as pd
import PyPDF2
import config
import matplotlib.pyplot as plt

# The following data science skill sets are modified from 
# https://github.com/yuanyuanshi/Data_Skills/blob/master/data_skills_1.py
program_languages = ['bash','r','python','java','c++','ruby','perl','matlab','javascript','scala','php']
analysis_software = ['excel','tableau','sas','spss','d3','saas','pandas','numpy','scipy','sps','spotfire','scikit','splunk','power','h2o']
ml_framework = ['pytorch','tensorflow','caffe','caffe2','cntk','mxnet','paddle','keras','bigdl']
bigdata_tool = ['hadoop','mapreduce','spark','pig','hive','shark','oozie','zookeeper','flume','mahout','etl']
ml_platform = ['aws','azure','google','ibm']
methodology = ['agile','devops','scrum']
databases = ['sql','nosql','hbase','cassandra','mongodb','mysql','mssql','postgresql','oracle','rdbms','bigquery']
overall_skills_dict = program_languages + analysis_software + ml_framework + bigdata_tool + databases + ml_platform + methodology
education = ['master','phd','undergraduate','bachelor','mba']
overall_dict = overall_skills_dict + education
jobs_info_df = pd.DataFrame()

class skill_keyword_match:
    def __init__(self, jobs_list):
        '''
        Initialization - converts list to DataFrame
        Input: 
            jobs_list (list): a list of all jobs info
        Output: 
            None
        '''
        self.jobs_info_df = pd.DataFrame(jobs_list)
          
    def keywords_extract(self, text): 
        '''
        Tokenize webpage text and extract keywords
        Input: 
            text (str): text to extract keywords from
        Output: 
            keywords (list): keywords extracted and filtered by pre-defined dictionary
        '''        
        # Remove non-alphabet; 3 for d3.js and + for C++
        text = re.sub("[^a-zA-Z+3]"," ", text) 
        text = text.lower().split()
        stops = set(stopwords.words("english")) #filter out stop words in english language
        text = [w for w in text if not w in stops]
        text = list(set(text))
        # We only care keywords from the pre-defined skill dictionary
        keywords = [str(word) for word in text if word in overall_dict]
        return keywords
 
    def keywords_count(self, keywords, counter): 
        '''
        Count frequency of keywords
        Input: 
            keywords (list): list of keywords
            counter (Counter)
        Output: 
            keyword_count (DataFrame index:keyword value:count)
        '''           
        keyword_count = pd.DataFrame(columns = ['Freq'])
        for each_word in keywords: 
            keyword_count.loc[each_word] = {'Freq':counter[each_word]}
        return keyword_count
    
    def exploratory_data_analysis(self):
        '''
        Exploratory data analysis
        Input: 
            None
        Output: 
            None
        '''         
        # Create a counter of keywords
        doc_freq = Counter() 
        f = [doc_freq.update(item) for item in self.jobs_info_df['keywords']]
        
        # Let's look up our pre-defined skillset vocabulary in Counter
        overall_skills_df = self.keywords_count(overall_skills_dict, doc_freq)
        # Calculate percentage of required skills in all jobs
        overall_skills_df['Freq_perc'] = (overall_skills_df['Freq'])*100/self.jobs_info_df.shape[0]
        overall_skills_df = overall_skills_df.sort_values(by='Freq_perc', ascending=False)  
        # Make bar plot 
        plt.figure(figsize=(14,8))
        overall_skills_df.iloc[0:30, overall_skills_df.columns.get_loc('Freq_perc')].plot.bar()
        plt.title('Percentage of Required Data Skills in Data Scientist/Engineer/Analyst Job Posts')
        plt.ylabel('Percentage Required in Jobs (%)')
        plt.xticks(rotation=30)
        plt.show()
         
        # Let's look up education requirements
        education_df = self.keywords_count(education, doc_freq)
        # Merge undergrad with bachelor
        education_df.loc['bachelor','Freq'] = education_df.loc['bachelor','Freq'] + education_df.loc['undergraduate','Freq'] 
        education_df.drop(labels='undergraduate', axis=0, inplace=True)
        # Calculate percentage of required skills in all jobs
        education_df['Freq_perc'] = (education_df['Freq'])*100/self.jobs_info_df.shape[0] 
        education_df = education_df.sort_values(by='Freq_perc', ascending=False)  
        # Make bar plot 
        plt.figure(figsize=(14,8))
        education_df['Freq_perc'].plot.bar()
        plt.title('Percentage of Required Education in Data Scientist/Engineer/Analyst Job Posts')
        plt.ylabel('Percentage Required in Jobs (%)')
        plt.xticks(rotation=0)
        plt.show()
        
        # Plot distributions of jobs posted in major cities 
        plt.figure(figsize=(8,8))
        self.jobs_info_df['location'].value_counts().plot.pie(autopct='%1.1f%%', textprops={'fontsize': 10})
        plt.title('Data Scientist/Engineer/Analyst Jobs in Major Canadian Cities \n\n Total {} posted jobs in last {} days'.format(self.jobs_info_df.shape[0],config.DAY_RANGE))
        plt.ylabel('')
        plt.show()
    
    def get_jaccard_sim(self, x_set, y_set): 
        '''
        Jaccard similarity or intersection over union measures similarity 
        between finite sample sets,  and is defined as size of intersection 
        divided by size of union of two sets. 
        Jaccard calculation is modified from 
        https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
        Input: 
            x_set (set)
            y_set (set)
        Output: 
            Jaccard similarity score
        '''         
        intersection = x_set.intersection(y_set)
        return float(len(intersection)) / (len(x_set) + len(y_set) - len(intersection))
    
    def cal_similarity(self, resume_keywords, location=None):
        '''
        Calculate similarity between keywords from resume and job posts
        Input: 
            resume_keywords (list): resume keywords
            location (str): city to search jobs
        Output: 
            top_match (DataFrame): top job matches
        '''         
        num_jobs_return = 5
        similarity = []
        j_info = self.jobs_info_df.loc[self.jobs_info_df['location']==location].copy() if len(location)>0 else self.jobs_info_df.copy()
        if j_info.shape[0] < num_jobs_return:        
            num_jobs_return = j_info.shape[0]  
        for job_skills in j_info['keywords']:
            similarity.append(self.get_jaccard_sim(set(resume_keywords), set(job_skills)))
        j_info['similarity'] = similarity
        top_match = j_info.sort_values(by='similarity', ascending=False).head(num_jobs_return)        
        # Return top matched jobs
        return top_match
      
    def extract_jobs_keywords(self):
        '''
        Extract skill keywords from job descriptions and add a new column 
        Input: 
            None
        Output: 
            None
        ''' 
        self.jobs_info_df['keywords'] = [self.keywords_extract(job_desc) for job_desc in self.jobs_info_df['desc']]
        
    def extract_resume_keywords(self, resume_pdf): 
        '''
        Extract key skills from a resume 
        Input: 
            resume_pdf (str): path to resume PDF file
        Output: 
            resume_skills (DataFrame index:keyword value:count): keywords counts
        ''' 
        # Open resume PDF
        resume_file = open(resume_pdf, 'rb')
        # creating a pdf reader object
        resume_reader = PyPDF2.PdfFileReader(resume_file)
        # Read in each page in PDF
        resume_content = [resume_reader.getPage(x).extractText() for x in range(resume_reader.numPages)]
        # Extract key skills from each page
        resume_keywords = [self.keywords_extract(page) for page in resume_content]
        # Count keywords
        resume_freq = Counter() 
        f = [resume_freq.update(item) for item in resume_keywords] 
        # Get resume skill keywords counts
        resume_skills = self.keywords_count(overall_skills_dict, resume_freq)
        
        return(resume_skills[resume_skills['Freq']>0])
