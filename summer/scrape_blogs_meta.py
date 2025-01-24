from bs4 import BeautifulSoup
import requests
import pandas as pd
from utils import *


def scrape_blogs_meta(cc):
    df = pd.read_csv(f'./data/{cc}/tmp_blog_links.csv')

    csv_blog_meta_lines = []
    for i, row in df.iterrows():    

        blog_url = row['blog_href']
        # print(blog_url)

    #     parse entire Page
        r = requests.get(blog_url)
        r_soup = BeautifulSoup(r.content, 'html.parser')

    #     n of comments
        n_comments_elem = r_soup.find(class_='comment-headline')
        n_comments = int(n_comments_elem.text.split()[0]) if n_comments_elem else None

    #     auther and publish_date
        meta_elem = r_soup.find(class_='post-meta')
        if meta_elem:
            meta_elem_p = meta_elem.find_all('p')
    #         extract author
            author = meta_elem_p[0].text.strip() if meta_elem_p else None

    #         extract publish_date
            if len(meta_elem_p) == 2:
                publish_date = meta_elem_p[1].text.strip() if len(meta_elem_p) == 2 else None
                # print(publish_date)
            else:
                publish_date = None


    #     participants_elem = page.html.find('.project-hero__project-size',first=True)
    #     category_elem = page.html.find('.project-hero__project-category',first=True)
    #     timespan_elem = page.html.find('.project-hero__project-runtime',first=True)

    #     participants = int(participants_elem.text.split()[0]) if participants_elem else None
    #     category = category_elem.text.strip() if category_elem else None
    #     timespan = timespan_elem.text.strip() if timespan_elem else None

        content_elem = r_soup.find(class_='post-content__article')
        content = r_soup.find(class_='post-content__article').text if content_elem else None

        csv_blog_meta_lines.append({
            'project_id' : row['project_id'],
            'blog_id' : row['blog_id'],
            'blog_href' : blog_url,
    #         'category' : category,
    #         'timespan' : timespan,
    #         'n_participants' : participants,
            'author' : author,
            'publish_date' : publish_date,
            'content' : content,
            'n_comments' : n_comments
        })

    #     break

    df = pd.DataFrame(csv_blog_meta_lines)
    df.to_csv(f'./data/{cc}/blogs_meta.csv', index=None)  