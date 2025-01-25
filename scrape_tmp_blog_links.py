import os
import sys
import datetime
import requests
import pandas as pd

import time
import csv
from tqdm import tqdm
from utils import *
from bs4 import BeautifulSoup


def scrape_tmp_blog_links(cc):

    df = pd.read_csv(f'./data/{cc}/projects.csv')
    csv_blog_line = []
    blog_id = 1

    # do this for all projects
    for i, row in df.iterrows():
    # tmp_list = list(df[::-1].iterrows())[99:]
    # for i, row in tmp_list:

    #     get the projects' url
        project_base_url = row['href']
        # project_base_url = "https://www.trnd.com/de/projekte/tiptoi-2021"
        # print(f'\n#{i+1}  {project_base_url}')
    #     request html from project and the parse it
        r = requests.get(project_base_url)
        if not r.ok:
            continue
            
        r_soup = BeautifulSoup(r.content, 'html.parser')

    #     try to get whatever is there, maybe a nav-bar or phase-wrapper
        # nav_bar = r_soup.find(class_='project-nav')
        blogs = r_soup.find_all(class_='CampaignBlogPostsPage')


        blog_links = []
    #     only do this if has nav bar
        # if nav_bar:
        #     # print([x.text for x in nav_bar.find_all('a')])
        #     # print(nav_bar.find_all('a'))
        #     if any([x.text == 'Blog' for x in nav_bar.find_all('a')]):
        #         blog_links.extend(get_blog_links_design1(f'{project_base_url}/blog'))
        #     if any([x.text == 'Projektblog' for x in nav_bar.find_all('a')]):
        #         project_blog_link = [x for x in nav_bar.find_all('a') if x.text == 'Projektblog'][0].attrs['href']
        #         blog_links.extend(get_blog_links_design1(project_blog_link))
        #     if len(blog_links) == 0 and any(['blog' in x.text.lower() for x in nav_bar.find_all('a')]):
        #         print(f"you didn't catch this one --> {x.text}")

    #     only do this if has phase-wrapper
        if len(blogs) > 0:
            # print(f"{len(phases)} " + f"phase wrappe {project_base_url}")
            blog_links.extend(get_blog_links_design2(blogs))

        # print(f"{len(blog_links)} found in this iteration")
        for link in blog_links:
            csv_blog_line.append({
                'project_id' : row['project_id'],
                'blog_id' : blog_id,
                'blog_href' : link

            })
            blog_id+=1
        # break
    df = pd.DataFrame(csv_blog_line)
    df.to_csv(f'./data/{cc}/tmp_blog_links.csv', index=None)