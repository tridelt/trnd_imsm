import os
import sys
import datetime
import requests
import pandas as pd

import time
import csv
from tqdm import tqdm
from bs4 import BeautifulSoup


def scrape_faq(cc):
    # this should work all the way back... 2017 and earlier
    df = pd.read_csv(f'./data/{cc}/projects.csv')

    csv_infos_line = []
    faq_id = 1
    for i, row in df.iterrows():

        project_base_url = row['href']

        r = requests.get(project_base_url)
        r_soup = BeautifulSoup(r.content, 'html.parser')

        faq_blog = r_soup.find(class_='CampaignBlogFaqPage')
        
        if not faq_blog:
            continue
        
        faq_bloglink = faq_blog['href']

        # print(f'#{i+1}  {project_faq_link}')
        r = requests.get(faq_bloglink)
        r_soup = BeautifulSoup(r.content, 'html.parser')

        faq_elements = r_soup.find_all(class_='faq-question')

        for faq_element in faq_elements:
            q = faq_element.find('h4')
            a = faq_element.find('p')

            if q and a:
                q = q.text
                a = a.text

                csv_infos_line.append({
                    'project_id' : row['project_id'],
                    'question_id' : faq_id,
                    'question' : q,
                    'answer' : a
                })
                faq_id+=1
    #     break

    df = pd.DataFrame(csv_infos_line)
    df.to_csv(f'./data/{cc}/faq.csv', index=None)