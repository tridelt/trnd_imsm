import os
import sys
import datetime
import requests
import pandas as pd

import time
import csv
from tqdm import tqdm
from bs4 import BeautifulSoup


def scrape_results(cc):
    # this should work all the way back... 2017 and earlier

    df = pd.read_csv(f'./data/{cc}/projects.csv')

    csv_result_line = []
    for i, row in df.iterrows():

        project_base_url = row['href']
        # print(f'\n#{i+1}  {project_base_url}')
        r = requests.get(project_base_url)
        r_soup = BeautifulSoup(r.content, 'html.parser')

        blog_results = r_soup.find(class_='CampaignBlogResultPage')
        
        if not blog_results:
            continue
            
        blog_results_link = blog_results['href']

        # print(f'#{i+1}  {project_results_link}')
        r = requests.get(blog_results_link)
        r_soup = BeautifulSoup(r.content, 'html.parser')
        
        content = r_soup.find(class_='post-wrapper')
        content = content.find('article').text if content else None

        # weiterempfehlungsquote
        weiterempfehlungsquote_elem = r_soup.find(class_='product-conviction__number')
        weiterempfehlungsquote = int(weiterempfehlungsquote_elem.text.strip()[:-1]) if weiterempfehlungsquote_elem else None

        spans = r_soup.find_all('span')
        rating_value = [item for item in spans if item.attrs.get('itemprop') == 'ratingValue']
        review_count = [item for item in spans if item.attrs.get('itemprop') == 'reviewCount']
        rating_value = float(rating_value[0].text) if len(rating_value) == 1 else None
        review_count = int(review_count[0].text.replace('.','')) if len(review_count) == 1 else None

        csv_result_line.append({
            'project_id' : row['project_id'],
            'weiterempfehlungsquote (%)' : weiterempfehlungsquote,
            'rating_value' : rating_value,
            'review_count' : review_count,
            'content' : content,
            'n_comments': 0
        })

    df = pd.DataFrame(csv_result_line)
    df.to_csv(f'./data/{cc}/results.csv', index=None)