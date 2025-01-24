from bs4 import BeautifulSoup
import requests
import pandas as pd
from utils import *
import os

from scrape_projects_meta import scrape_projects_meta
from scrape_faq import scrape_faq
from scrape_results import scrape_results
from scrape_tmp_blog_links import scrape_tmp_blog_links
from scrape_blogs_meta import scrape_blogs_meta
from comments_module import scrape_comments


# run status quo and just see where someething isn't working
for cc in ['de', 'be-fr', 'be-nl', 'cz', 'es', 'fr', 'it', 'hu', 'nl', 'pl', 'pt', 'ro', 'uk']:
    if not os.path.isdir(f"./data/{cc}"):
        os.mkdir(f"./data/{cc}")

#     scrape PROJECTS
    if not os.path.isfile(f"./data/{cc}/projects.csv"):
        scrape_projects_meta(cc)
    print(f"scraped PROJECTS --> {cc}")

#     scrape FAQ based on PROJECTS
    if not os.path.isfile(f"./data/{cc}/faq.csv"):
        scrape_faq(cc)
    print(f"scraped FAQ --> {cc}")

#     scrape RESULTS based on PROJECTS
    if not os.path.isfile(f"./data/{cc}/results.csv"):
        scrape_results(cc)
    print(f"scraped RESULTS --> {cc}")

#     scrape tmp-BLOG-LINKS based on PROJECTS
    if not os.path.isfile(f"./data/{cc}/tmp_blog_links.csv"):
        scrape_tmp_blog_links(cc)
    print(f"scraped TMP_BLOG_LINKS --> {cc}")

#     scrape BLOG-META based on tmp-BLOG-LINKS
    if not os.path.isfile(f"./data/{cc}/blogs_meta.csv"):
        scrape_blogs_meta(cc)
        count_comments(cc)
        print(f"added n_comments to results.csv --> {cc}")
    print(f"scraped BLOGS_META --> {cc}")

#     scrape BLOG-COMMENTS based on tmp-BLOG-LINKS
    if not os.path.isfile(f"./data/{cc}/blogs_comments.csv"):
        scrape_comments(cc)
    print(f"scraped BLOGS_COMMENTS --> {cc}")

    # breaks