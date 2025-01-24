from bs4 import BeautifulSoup
import requests
import pandas as pd
from utils import *


def scrape_blogs_comments(cc):
    df = pd.read_csv(f'./data/{cc}/tmp_blog_links.csv')

    csv_comment_lines = []
    # comment_id = 675675
    comment_id = 1
    for i, row in df.iterrows():
    #     if row['blog_id'] <= 2267:
    #         continue
        comments_parsed = parse_blog(row['blog_href'])
        # print(f'#{len(comments_parsed)}  --  {row["blog_href"]}')

        for comment_parsed in comments_parsed:
            comment_parsed['project_id'] = row['project_id']
            comment_parsed['blog_id'] = row['blog_id']
            comment_parsed['comment_id'] = comment_id

            csv_comment_lines.append(comment_parsed)
            comment_id+=1

    df = pd.DataFrame(csv_comment_lines)
    df = df.reindex(['project_id','blog_id','comment_id','comment_author','comment_time','comment_text','reply_to','is_moderator'],axis=1)
    df = df.sort_values(by=['blog_id','comment_id'],ascending=[True,True])
    df.to_csv(f'./data/{cc}/blogs_comments.csv', index=None)
